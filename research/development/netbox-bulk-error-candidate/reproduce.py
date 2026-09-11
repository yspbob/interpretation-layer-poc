"""Investigator reproduction against real NetBox, PostgreSQL and Redis.

No model calls, business logic replacements, or outgoing webhook workers.
Use only the disposable database named below. Observed rule failures are data;
an inability to run the check or a failed positive control fails the command.
"""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import traceback


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    os.environ["DJANGO_SETTINGS_MODULE"] = "netbox.settings"
    os.environ["NETBOX_CONFIGURATION"] = "nb_bulk_configuration"
    sys.path.insert(0, str(source / "netbox"))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    report = {
        "kind": "public investigator runtime reproduction, not model evaluation",
        "source_revision": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=source, text=True
        ).strip(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "configuration_sha256": hashlib.sha256(
            Path(__file__).with_name("nb_bulk_configuration.py").read_bytes()
        ).hexdigest(),
        "python": platform.python_version(),
        "packages": dict(sorted((d.metadata["Name"], d.version)
                                for d in importlib.metadata.distributions())),
        "ci_run_id": os.environ.get("GITHUB_RUN_ID"),
        "ci_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "poc_revision": os.environ.get("GITHUB_SHA"),
        "scenarios": [],
        "completed": False,
        "limits": [
            "Tests synchronous Site PATCH requests as a superuser only.",
            "Measures real queued webhook jobs, not execution or remote delivery.",
            "No workers start. Webhook target is loopback only.",
            "No model, guidance assessment, or agent containment test.",
        ],
    }
    try:
        import django
        django.setup()
        from django.conf import settings
        from django.contrib.auth import get_user_model
        from django.core.management import call_command
        from django.db import connection
        from rest_framework.test import APIClient
        import django_rq
        from core.events import OBJECT_UPDATED
        from core.models import ObjectType, ObjectChange
        from dcim.models import Site
        from extras.choices import EventRuleActionChoices
        from extras.models import EventRule, Webhook

        assert settings.DATABASES["default"]["NAME"] == "netbox_nb_bulk_reproduction"
        assert settings.DATABASES["default"]["HOST"] in ("localhost", "127.0.0.1", "postgres")
        assert not connection.in_atomic_block
        call_command("migrate", interactive=False, verbosity=1)
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            report["postgresql"] = cursor.fetchone()[0]
        queue = django_rq.get_queue("default")
        report["redis"] = queue.connection.info("server")["redis_version"]
        assert not queue.connection.smembers("rq:workers"), "No workers may deliver webhooks"
        user = get_user_model().objects.create_superuser(username="nb-bulk-investigator")
        webhook = Webhook.objects.create(
            name="Local reproduction only", payload_url="http://127.0.0.1:9/never-deliver"
        )
        rule = EventRule.objects.create(
            name="Site update reproduction", event_types=[OBJECT_UPDATED],
            action_type=EventRuleActionChoices.WEBHOOK,
            action_object_type=ObjectType.objects.get_for_model(Webhook),
            action_object_id=webhook.pk,
        )
        rule.object_types.set([ObjectType.objects.get_for_model(Site)])
        client = APIClient()
        client.force_authenticate(user=user)
        # Site's native ordering is name. Each request uses that same order.
        scenarios = [
            ("success", [True, True]),
            ("valid_then_invalid", [True, False]),
            ("invalid_then_valid", [False, True]),
            ("both_invalid", [False, False]),
        ]
        for index, (name, valid) in enumerate(scenarios):
            queue.empty()
            sites = [Site.objects.create(
                name=f"Reproduction {index} {letter}", slug=f"repro-{index}-{letter}",
                description="original", status="active"
            ) for letter in ("A", "B")]
            ids = [site.pk for site in sites]
            baseline_changes = ObjectChange.objects.count()
            request = [dict(id=site.pk, description="edited",
                            **({} if ok else {"status": "not-a-valid-site-status"}))
                       for site, ok in zip(sites, valid)]
            response = client.patch("/api/dcim/sites/", request, format="json")
            state = list(Site.objects.filter(pk__in=ids).order_by("name")
                         .values("id", "name", "status", "description"))
            jobs = [{"function": job.func_name,
                     "event_type": job.kwargs.get("event_type"),
                     "data": job.kwargs.get("data"),
                     "snapshots": job.kwargs.get("snapshots")}
                    for job in queue.jobs]
            changed = sum(item["description"] != "original" for item in state)
            changes = ObjectChange.objects.count() - baseline_changes
            success = all(valid)
            row = {
                "name": name, "request": request, "http_status": response.status_code,
                "response": response.json(), "database_after": state,
                "changed_rows": changed, "change_log_rows_added": changes,
                "queued_webhook_jobs": jobs, "queued_job_count": len(jobs),
                "required": {"http_status": 200 if success else 400,
                             "changed_rows": 2 if success else 0,
                             "queued_job_count": 2 if success else 0},
                "transaction_open_after_request": connection.in_atomic_block,
            }
            row["satisfies_scoped_rule"] = (
                response.status_code == row["required"]["http_status"]
                and changed == row["required"]["changed_rows"]
                and len(jobs) == row["required"]["queued_job_count"]
                and changes == (2 if success else 0)
            )
            report["scenarios"].append(row)
            assert response.status_code == (200 if success else 400), row
            assert changed == (2 if success else 0), row
            assert changes == (2 if success else 0), row
            assert not connection.in_atomic_block
            assert all(job["function"] == "extras.webhooks.send_webhook" for job in jobs)
            if success:
                assert len(jobs) == 2, "Positive control must dispatch both real webhook jobs"
                assert {job["data"]["id"] for job in jobs} == set(ids)
                assert all(job["data"]["description"] == "edited" for job in jobs)
            print(json.dumps({key: row[key] for key in
                              ("name", "http_status", "changed_rows", "queued_job_count",
                               "satisfies_scoped_rule")}))
            queue.empty()
        report["completed"] = True
    except Exception:
        report["fatal_error"] = traceback.format_exc()
        raise
    finally:
        output.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
