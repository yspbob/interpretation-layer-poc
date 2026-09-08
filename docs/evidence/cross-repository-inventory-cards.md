# Cross-repository decision inventory — case cards

84 exploratory records. Advance means develop a fixture, not validated benchmark eligibility. The original twelve NetBox cases are marked; all records contain possible answers and must be excluded from experimental drafter inputs.

Disposition meanings: advance = substantive candidate; control = uncertainty/authority/conflict; defer = unresolved evidence; calibration = easy local behavior; merge = challenge of an existing family; reject = outside substantive scope.

## netbox

### N01 — Brief serializers, stale guidance and retained special cases

**Disposition:** control · **Family:** netbox/serializer-representation · **Original development case**

**Reference:** [N01: docs/plugins/development/migration-v4.md:227](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/plugins/development/migration-v4.md#L227)

**Bounded interpretation:** Ordinary nested relationships can reuse primary serializers using nested=True and brief_fields; specialised nested serializers still exist. Identify the conflicting style guide if documents are available.

**Challenge:** Ordinary related object versus specialised representation; identify the allowed route without banning every retained class.

**Screening reason:** Conflict case: competing documentation and retained exceptions.

**Implementation anchors:** [netbox/netbox/api/serializers/base.py:17](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/api/serializers/base.py#L17), [netbox/ipam/api/serializers_/asns.py:16](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/ipam/api/serializers_/asns.py#L16), [netbox/ipam/api/serializers_/nested.py:13](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/ipam/api/serializers_/nested.py#L13)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N02 — Model validation belongs in clean with inherited validation retained

**Disposition:** advance · **Family:** netbox/model-validation · **Original development case**

**Reference:** [N02: docs/development/extending-models.md:34](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/development/extending-models.md#L34)

**Bounded interpretation:** Model-level additional validation uses clean and calls inherited clean; callers still need a validation path such as full_clean.

**Challenge:** Add a model invariant used through multiple entry points; retain inherited validation.

**Screening reason:** Model validation and inherited behavior; source access and realistic caller fixture required.

**Implementation anchors:** [netbox/dcim/models/racks.py:39](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/dcim/models/racks.py#L39), [netbox/dcim/models/sites.py:24](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/dcim/models/sites.py#L24), [netbox/netbox/models/__init__.py:25](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/models/__init__.py#L25), [netbox/netbox/api/serializers/base.py:17](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/api/serializers/base.py#L17)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N03 — Feature composition permits both full and selective mixins

**Disposition:** advance · **Family:** netbox/feature-composition · **Original development case**

**Reference:** [N03: docs/plugins/development/models.md:69](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/plugins/development/models.md#L69)

**Bounded interpretation:** NetBoxModel bundles features; a plugin can compose a subset using feature mixins and a Django model base. Feature registration follows inheritance.

**Challenge:** A plugin model requiring only two features must not be forced into the full feature bundle.

**Screening reason:** Selective capability composition, rather than compulsory full base class.

**Implementation anchors:** [netbox/netbox/models/__init__.py:25](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/models/__init__.py#L25), [netbox/netbox/models/features.py:49](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/models/features.py#L49)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N04 — ObjectType convention has a GenericForeignKey exception

**Disposition:** advance · **Family:** netbox/content-type-boundary · **Original development case**

**Reference:** [N04: docs/plugins/development/migration-v4.md:25](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/plugins/development/migration-v4.md#L25)

**Bounded interpretation:** Use the ObjectType proxy for ordinary object-type operations; the concrete content-type FK backing a generic relationship points to Django ContentType.

**Challenge:** Compare a feature-selection relation and a GenericForeignKey backing field.

**Screening reason:** Concrete/proxy exception at generic relationship boundary.

**Implementation anchors:** [netbox/core/models/contenttypes.py:12](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/core/models/contenttypes.py#L12), [netbox/extras/models/customfields.py:53](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/extras/models/customfields.py#L53), [netbox/tenancy/models/contacts.py:20](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/tenancy/models/contacts.py#L20), [netbox/extras/models/models.py:45](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/extras/models/models.py#L45)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N05 — Private model flag controls catalogue inclusion, not blanket authorisation

**Disposition:** advance · **Family:** netbox/model-catalogue · **Original development case**

**Reference:** [N05: docs/plugins/development/models.md:65](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/plugins/development/models.md#L65)

**Bounded interpretation:** _netbox_private excludes the model from registry[models] and the public object-type catalogue. Feature registration is a separate loop.

**Challenge:** A hidden support model can retain feature registration; distinguish catalogue hiding from permissions.

**Screening reason:** Catalogue visibility is separate from access control.

**Implementation anchors:** [netbox/netbox/models/features.py:49](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/models/features.py#L49), [netbox/core/models/contenttypes.py:12](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/core/models/contenttypes.py#L12), [netbox/extras/models/tags.py:24](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/extras/models/tags.py#L24)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N06 — Script dry-run rollback is bounded to database transaction behaviour

**Disposition:** advance · **Family:** netbox/script-transactions · **Original development case**

**Reference:** [N06: docs/customization/custom-scripts.md:51](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/customization/custom-scripts.md#L51)

**Bounded interpretation:** ScriptJob wraps the call in a transaction and aborts that transaction when commit is false. This does not establish rollback of emails, files, network calls or every database connection.

**Challenge:** A script writes a model and emits an external event: distinguish which operation is protected.

**Screening reason:** Database transaction boundary does not cover arbitrary external effects.

**Implementation anchors:** [netbox/extras/jobs.py:16](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/extras/jobs.py#L16), [netbox/extras/scripts.py:51](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/extras/scripts.py#L51), [netbox/utilities/exceptions.py:13](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/utilities/exceptions.py#L13)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N07 — Field propagation depends on intended surfaces

**Disposition:** control · **Family:** netbox/field-propagation · **Original development case**

**Reference:** [N07: docs/development/extending-models.md:66](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/development/extending-models.md#L66)

**Bounded interpretation:** Consider API, forms, filters, tables and search; update each surface when required by the field purpose. Code can reveal existing mappings, not every future product requirement.

**Challenge:** One field is internal-only, another must be editable and filterable; compare obligations supplied in each task.

**Screening reason:** Exposure depends on intended use; no universal every-field-everywhere rule.

**Implementation anchors:** [netbox/dcim/models/sites.py:24](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/dcim/models/sites.py#L24), [netbox/dcim/api/serializers_/sites.py:21](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/dcim/api/serializers_/sites.py#L21), [netbox/dcim/forms/filtersets.py:63](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/dcim/forms/filtersets.py#L63), [netbox/dcim/filtersets.py:86](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/dcim/filtersets.py#L86), [netbox/dcim/tables/sites.py:22](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/dcim/tables/sites.py#L22)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N08 — Registry mutability contract and enforcement gap

**Disposition:** control · **Family:** netbox/registry-enforcement · **Original development case**

**Reference:** [N08: docs/development/application-registry.md:5](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/development/application-registry.md#L5)

**Bounded interpretation:** Normal item assignment/deletion is blocked while nested store values remain mutable. The documented intent is stronger than enforcement through inherited dict methods.

**Challenge:** Contrast item replacement, nested mutation and inherited update; flag the implementation gap rather than invent permission to bypass.

**Screening reason:** Local dictionary enforcement gap; useful conflict control, not headline architecture.

**Implementation anchors:** [netbox/netbox/registry.py:5](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/registry.py#L5), [netbox/netbox/models/features.py:49](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/models/features.py#L49)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N09 — Supported plugin API is a compatibility commitment

**Disposition:** control · **Family:** netbox/api-authority · **Original development case**

**Reference:** [N09: docs/plugins/development/index.md:26](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/plugins/development/index.md#L26)

**Bounded interpretation:** Code reveals importable interfaces and usage. Without the support-policy record, it cannot establish the exact documented compatibility boundary; request authority.

**Challenge:** An importable internal utility is convenient; code-only answer must not promise long-term compatibility.

**Screening reason:** Hidden compatibility promise cannot be established by code.

**Implementation anchors:** [netbox/netbox/plugins/__init__.py:43](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/plugins/__init__.py#L43), [netbox/netbox/models/__init__.py:25](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/models/__init__.py#L25)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N10 — Dependency acceptance includes a one-year maintenance criterion

**Disposition:** control · **Family:** netbox/dependency-authority · **Original development case**

**Reference:** [N10: docs/development/style-guide.md:58](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/development/style-guide.md#L58)

**Bounded interpretation:** Pins and existing dependencies are observable; the release-age threshold, licence acceptability and procurement rationale require external policy evidence.

**Challenge:** Two otherwise similar dependencies differ in release age; code alone cannot supply the governing cutoff.

**Screening reason:** Hidden dependency threshold cannot be established from installed versions.

**Implementation anchors:** [base_requirements.txt:1](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/base_requirements.txt#L1), [requirements.txt:1](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/requirements.txt#L1)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N11 — Released migrations have a policy exception for bug correction

**Disposition:** control · **Family:** netbox/migration-authority · **Original development case**

**Reference:** [N11: docs/development/extending-models.md:30](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/development/extending-models.md#L30)

**Bounded interpretation:** A code snapshot does not establish release status or the authorised bug-correction exception; request the policy and release history.

**Challenge:** Contrast unreleased consolidation and a released migration bug; neither authority can be invented from file age.

**Screening reason:** Released migration policy and its exception require external authority.

**Implementation anchors:** [netbox/dcim/migrations/0188_racktype.py:11](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/dcim/migrations/0188_racktype.py#L11)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N12 — Pre-change snapshots precede edits for correct change logging

**Disposition:** advance · **Family:** netbox/change-logging · **Original development case**

**Reference:** [N12: docs/customization/custom-scripts.md:221](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/customization/custom-scripts.md#L221)

**Bounded interpretation:** For an existing object supporting change logging, capture the pre-edit state before mutation so the change record has the correct before state. Some managed paths do this centrally.

**Challenge:** Compare manual script mutation with a managed path that already captures the snapshot; detect late snapshots.

**Screening reason:** Pre-edit state capture with managed-path exceptions.

**Implementation anchors:** [netbox/netbox/models/features.py:49](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/models/features.py#L49), [netbox/netbox/api/viewsets/__init__.py:34](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/api/viewsets/__init__.py#L34), [netbox/core/signals.py:1](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/core/signals.py#L1), [netbox/dcim/models/racks.py:39](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/dcim/models/racks.py#L39)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N13 — Permission constraint composition

**Disposition:** advance · **Family:** netbox/permissions

**Reference:** [N13: docs/administration/permissions.md:32](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/administration/permissions.md#L32)

**Bounded interpretation:** Conditions within an object intersect; alternative objects and applicable permission grants combine as alternatives.

**Challenge:** Distinguish two restrictive attributes in one grant from two separate grants; do not accidentally turn an OR into an AND.

**Screening reason:** Crosses permission collection and query construction; related to N14, not an independent subsystem.

**Implementation anchors:** [netbox/utilities/permissions.py:86](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/utilities/permissions.py#L86), [netbox/netbox/authentication/__init__.py:92](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/authentication/__init__.py#L92)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N14 — Permission checks on the resulting saved state

**Disposition:** advance · **Family:** netbox/permissions

**Reference:** [N14: docs/administration/permissions.md:113](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/administration/permissions.md#L113)

**Bounded interpretation:** For these API writes, save and check the resulting restricted queryset inside a transaction so changes that escape allowed scope are rolled back.

**Challenge:** Move an otherwise editable object outside its permitted region; contrast a valid in-scope update.

**Screening reason:** Causal transaction and access-control interaction; limit claims to inspected write paths.

**Implementation anchors:** [netbox/netbox/api/viewsets/__init__.py:166](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/api/viewsets/__init__.py#L166), [netbox/netbox/api/viewsets/__init__.py:186](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/api/viewsets/__init__.py#L186)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N15 — Outbound event actions are deferred selectively

**Disposition:** advance · **Family:** netbox/background-events

**Reference:** [N15: docs/features/event-rules.md:32](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/features/event-rules.md#L32)

**Bounded interpretation:** Webhook delivery and custom-script execution are enqueued; event-rule evaluation and notification creation are not universally moved to a worker by this code.

**Challenge:** A slow outbound webhook versus an in-process notification action; do not generalize queueing to every step of event processing.

**Screening reason:** Source narrows the broad documentation: inspect each action branch. Supports a scoped request/worker boundary, not blanket asynchronous execution.

**Implementation anchors:** [netbox/extras/events.py:156](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/extras/events.py#L156), [netbox/extras/events.py:121](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/extras/events.py#L121)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N16 — Idempotent scheduling with explicit on-demand jobs

**Disposition:** advance · **Family:** netbox/job-scheduling

**Reference:** [N16: docs/plugins/development/background-jobs.md:43](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/plugins/development/background-jobs.md#L43)

**Bounded interpretation:** Schedule creation checks pending jobs under an advisory lock; on-demand enqueue remains permitted and a changed schedule can replace a pending one.

**Challenge:** Concurrent repeated schedule requests versus an explicit immediate job; reject a universal one-job-ever rule.

**Screening reason:** Substantive concurrency and lifecycle interpretation; runnable concurrency fixture still needed.

**Implementation anchors:** [netbox/netbox/jobs.py:130](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/jobs.py#L130), [netbox/netbox/jobs.py:129](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/jobs.py#L129)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N17 — Plugin queues require workers that service them

**Disposition:** advance · **Family:** netbox/job-scheduling

**Reference:** [N17: docs/plugins/development/background-jobs.md:127](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/plugins/development/background-jobs.md#L127)

**Bounded interpretation:** Defining a custom plugin queue does not itself establish that a worker services it; queue configuration and worker subscription are separate.

**Challenge:** A successfully enqueued plugin task never executes under default worker subscriptions.

**Screening reason:** Boundary between application registration and deployment; must include worker configuration as allowed evidence.

**Implementation anchors:** [netbox/netbox/settings.py:766](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/settings.py#L766), [netbox/core/management/commands/rqworker.py:8](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/core/management/commands/rqworker.py#L8)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N18 — Custom fields stored alongside model records

**Disposition:** calibration · **Family:** netbox/custom-fields

**Reference:** [N18: docs/customization/custom-fields.md:7](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/customization/custom-fields.md#L7)

**Bounded interpretation:** Custom field values are stored in the object's JSON field, separate from the definitions of those fields.

**Challenge:** Distinguish per-object values from field definitions; do not invent a measured performance benefit.

**Screening reason:** Storage representation is mostly local extraction; published performance rationale needs separate attribution.

**Implementation anchors:** [netbox/netbox/models/features.py:166](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/models/features.py#L166)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N19 — System-job registration depends on importing its module

**Disposition:** advance · **Family:** netbox/plugin-startup

**Reference:** [N19: docs/plugins/development/background-jobs.md:93](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/plugins/development/background-jobs.md#L93)

**Bounded interpretation:** A registration decorator takes effect when its module is imported; plugin startup must make declared system jobs reachable.

**Challenge:** Add a valid decorated job in an unimported module, then contrast startup that imports it.

**Screening reason:** Crosses declaration and initialization; source discovery alone cannot show a job is registered.

**Implementation anchors:** [netbox/netbox/jobs.py:21](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/jobs.py#L21), [netbox/netbox/plugins/__init__.py:100](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/plugins/__init__.py#L100)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N20 — Custom-field requiredness and defaults

**Disposition:** advance · **Family:** netbox/custom-fields

**Reference:** [N20: docs/customization/custom-fields.md:29](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/customization/custom-fields.md#L29)

**Bounded interpretation:** Custom field definitions and model validation jointly constrain values; requiredness applies to relevant saves and defaults do not make every supplied value valid.

**Challenge:** Save a required field missing, with a valid default, and with an invalid explicit value through a validation-aware path.

**Screening reason:** Schema/data interaction; avoid claiming every raw ORM save performs validation.

**Implementation anchors:** [netbox/netbox/models/features.py:162](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/netbox/models/features.py#L162), [netbox/extras/models/customfields.py:662](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/netbox/extras/models/customfields.py#L662)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### N21 — Final newline style rule

**Disposition:** reject · **Family:** netbox/formatting

**Reference:** [N21: docs/development/style-guide.md:13](https://github.com/netbox-community/netbox/blob/ea4c205a37baa3e58e6e481158c15c6154cceeff/docs/development/style-guide.md#L13)

**Bounded interpretation:** The project asks for a final newline.

**Challenge:** A file with or without a trailing newline.

**Screening reason:** A linter-level formatting rule adds little evidence about substantive interpretation; rejected from the architecture inventory.

## wagtail

### W01 — Page permissions propagate down the tree

**Disposition:** advance · **Family:** wagtail/page-permissions

**Reference:** [W01: docs/topics/permissions.md:26](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/permissions.md#L26)

**Bounded interpretation:** A grant at an ancestor governs descendants; a root grant reaches the whole tree subject to other action-specific checks.

**Challenge:** A user edits a descendant but not a sibling outside the granted subtree.

**Screening reason:** Structural scope with a meaningful negative case.

**Implementation anchors:** [wagtail/permission_policies/pages.py:9](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/permission_policies/pages.py#L9), [wagtail/models/pages.py:2324](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/pages.py#L2324)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W02 — Add permission combines with page ownership

**Disposition:** advance · **Family:** wagtail/page-permissions

**Reference:** [W02: docs/topics/permissions.md:28](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/permissions.md#L28)

**Bounded interpretation:** Add permission can allow editing owned pages; deletion has additional subtree and publication checks, so edit permission alone is not an unconditional deletion guarantee.

**Challenge:** An editor creates drafts, edits their own draft, and tries to delete a live subtree without publishing rights.

**Screening reason:** Reference language requires qualification against code; grouped with W01.

**Implementation anchors:** [wagtail/models/pages.py:2365](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/pages.py#L2365), [wagtail/models/pages.py:2390](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/pages.py#L2390)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W03 — Chooser visibility is not content secrecy

**Disposition:** advance · **Family:** wagtail/asset-access

**Reference:** [W03: docs/topics/permissions.md:52](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/permissions.md#L52)

**Bounded interpretation:** Choose permissions filter selection interfaces; reading document contents has separate privacy and serving requirements, and image secrecy is not established by the chooser.

**Challenge:** A hidden chooser item is referenced directly; evaluate content-serving checks separately.

**Screening reason:** Distinct UI and content access boundaries; never score UI filtering as full authorization.

**Implementation anchors:** [wagtail/permission_policies/collections.py:207](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/permission_policies/collections.py#L207), [wagtail/documents/views/serve.py:18](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/documents/views/serve.py#L18), [wagtail/documents/wagtail_hooks.py:165](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/documents/wagtail_hooks.py#L165)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W04 — Document privacy depends on the serving route

**Disposition:** advance · **Family:** wagtail/asset-access

**Reference:** [W04: docs/advanced_topics/documents/storing_and_serving.md:33](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/advanced_topics/documents/storing_and_serving.md#L33)

**Bounded interpretation:** Application serving checks cannot protect a file also exposed by a direct storage URL; deployment configuration is part of the boundary.

**Challenge:** Compare protected serve_view access with a publicly reachable storage URL.

**Screening reason:** Requires controlled storage fixture; application code alone cannot prove deployment privacy.

**Implementation anchors:** [wagtail/documents/views/serve.py:18](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/documents/views/serve.py#L18), [wagtail/documents/models.py:165](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/documents/models.py#L165), [wagtail/documents/wagtail_hooks.py:165](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/documents/wagtail_hooks.py#L165)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W05 — Collection management cannot remove its permission anchor

**Disposition:** advance · **Family:** wagtail/collection-management

**Reference:** [W05: docs/topics/permissions.md:66](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/permissions.md#L66)

**Bounded interpretation:** Management grants allow operations below their anchor; deleting a collection also requires it to be empty and childless.

**Challenge:** Delete an empty descendant versus the grant anchor or a collection with descendants.

**Screening reason:** Permission scope interacts with hierarchy integrity.

**Implementation anchors:** [wagtail/permission_policies/collections.py:391](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/permission_policies/collections.py#L391), [wagtail/admin/views/collections.py:134](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/admin/views/collections.py#L134)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W06 — Revision persistence needs clustered relationships

**Disposition:** defer · **Family:** wagtail/revision-content

**Reference:** [W06: docs/topics/snippets/features.md:151](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/snippets/features.md#L151)

**Bounded interpretation:** Revision serialization must include unsaved child and many-to-many state; documented clustered relationships support that boundary.

**Challenge:** Save a draft with changed child relations and compare restored content with ordinary database relations.

**Screening reason:** Key semantics live in django-modelcluster, not this checkout; dependency source must be pinned and audited before advancing.

**Implementation anchors:** [wagtail/models/revisions.py:384](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/revisions.py#L384), [wagtail/models/revisions.py:346](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/revisions.py#L346)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W07 — Draft snippets need explicit live filtering at use sites

**Disposition:** advance · **Family:** wagtail/snippet-publishing

**Reference:** [W07: docs/topics/snippets/features.md:253](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/snippets/features.md#L253)

**Bounded interpretation:** A snippet's draft state does not automatically exclude it from all page rendering; consumers must apply the intended live-state handling.

**Challenge:** Render a page referencing an unpublished snippet and compare a live-aware implementation.

**Screening reason:** Lifecycle state versus downstream consumption; no universal enforcement inferred from the mixin.

**Implementation anchors:** [wagtail/models/draft_state.py:13](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/draft_state.py#L13), [wagtail/snippets/views/snippets.py:508](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/snippets/views/snippets.py#L508)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W08 — Workflow support composes revisions and publishing

**Disposition:** advance · **Family:** wagtail/workflow-composition

**Reference:** [W08: docs/topics/snippets/features.md:296](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/snippets/features.md#L296)

**Bounded interpretation:** Workflow-enabled models require revision and draft-state support in the appropriate inheritance order; locking is recommended rather than universally mandatory.

**Challenge:** A workflow mixin on a plain model versus the complete required composition; permit omission of optional locking.

**Screening reason:** Dependency and exception reasoning, with existing checks as evaluator evidence kept out of drafter inputs.

**Implementation anchors:** [wagtail/models/workflows.py:1196](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/workflows.py#L1196), [wagtail/models/draft_state.py:56](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/draft_state.py#L56)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W09 — Lockable mixin ordering

**Disposition:** merge · **Family:** wagtail/workflow-composition

**Reference:** [W09: docs/topics/snippets/features.md:284](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/snippets/features.md#L284)

**Bounded interpretation:** Lockable and revision mixins have an enforced ordering when composed.

**Challenge:** Swap mixin order while keeping names unchanged.

**Screening reason:** Merge into W08 as a challenge variant; do not count it as an independent architectural decision.

**Implementation anchors:** [wagtail/models/locking.py:40](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/locking.py#L40)

### W10 — Translation identity is shared across locales

**Disposition:** advance · **Family:** wagtail/translation

**Reference:** [W10: docs/advanced_topics/i18n.md:70](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/advanced_topics/i18n.md#L70)

**Bounded interpretation:** Translation siblings share a key but each locale permits only one member; identity is not determined by title or path alone.

**Challenge:** Create a second translation in the same locale versus a translation in a new locale.

**Screening reason:** Data invariant connected to lookup behavior.

**Implementation anchors:** [wagtail/models/i18n.py:177](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/i18n.py#L177), [wagtail/models/i18n.py:287](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/i18n.py#L287)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W11 — Locale-specific page trees and homepages

**Disposition:** advance · **Family:** wagtail/translation

**Reference:** [W11: docs/advanced_topics/i18n.md:78](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/advanced_topics/i18n.md#L78)

**Bounded interpretation:** Wagtail's built-in locale model uses related pages in locale-specific trees, with routing selecting the appropriate translated homepage.

**Challenge:** Two locale homepages with different child structures; avoid assuming every page must have a translated counterpart.

**Screening reason:** Crosses tree and routing; correlated with W10, not a new repository-level replication.

**Implementation anchors:** [wagtail/models/pages.py:1410](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/pages.py#L1410), [wagtail/models/i18n.py:247](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/models/i18n.py#L247)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W12 — Rich-text storage is distinct from rendered HTML

**Disposition:** advance · **Family:** wagtail/rich-text

**Reference:** [W12: docs/extending/rich_text_internals.md:20](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/extending/rich_text_internals.md#L20)

**Bounded interpretation:** Stored rich text retains entity references and must be expanded for rendering; final HTML is not the full storage contract.

**Challenge:** A stored page link after the target URL changes; compare reference expansion with a hard-coded URL.

**Screening reason:** Representation boundary with a meaningful lifecycle challenge.

**Implementation anchors:** [wagtail/rich_text/__init__.py:52](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/rich_text/__init__.py#L52), [wagtail/rich_text/rewriters.py:173](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/rich_text/rewriters.py#L173)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W13 — StreamField block validation is a form-layer operation

**Disposition:** advance · **Family:** wagtail/stream-validation

**Reference:** [W13: docs/advanced_topics/streamfield_validation.md:36](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/advanced_topics/streamfield_validation.md#L36)

**Bounded interpretation:** Block clean methods perform recursive validation through the form field; model full_clean alone does not establish valid block content.

**Challenge:** Insert invalid block content programmatically versus through BlockField validation.

**Screening reason:** Boundary and recursive validation; include draft deferred-validation conditions in fixture review.

**Implementation anchors:** [wagtail/blocks/base.py:790](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/blocks/base.py#L790), [wagtail/blocks/struct_block.py:311](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/blocks/struct_block.py#L311), [wagtail/fields.py:110](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/fields.py#L110)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W14 — Search indexes require synchronization with model changes

**Disposition:** defer · **Family:** wagtail/search-indexing

**Reference:** [W14: docs/topics/search/indexing.md:17](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/search/indexing.md#L17)

**Bounded interpretation:** Automatic index updates use configured signals and can be disabled; bulk or alternate write paths require checking whether those hooks run.

**Challenge:** Ordinary save versus a write path that bypasses signals; contrast explicit rebuild.

**Screening reason:** At this snapshot the implementation is re-exported from modelsearch. Pin and inspect that dependency and backend before advancing; local import stubs are insufficient evidence.

**Implementation anchors:** [wagtail/search/signal_handlers.py:1](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/search/signal_handlers.py#L1), [wagtail/search/index.py:1](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/search/index.py#L1)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W15 — Search fields and filter fields serve different purposes

**Disposition:** defer · **Family:** wagtail/search-indexing

**Reference:** [W15: docs/topics/search/indexing.md:125](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/search/indexing.md#L125)

**Bounded interpretation:** A filter field is not automatically a full-text search field.

**Challenge:** Search a field registered only for filtering.

**Screening reason:** A mostly local interface distinction, with its actual classes now supplied by modelsearch; defer pending dependency evidence and likely retain only as calibration.

**Implementation anchors:** [wagtail/search/index.py:1](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/search/index.py#L1)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W16 — Renditions preserve originals and reuse derived representations

**Disposition:** advance · **Family:** wagtail/image-renditions

**Reference:** [W16: docs/advanced_topics/images/renditions.md:6](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/advanced_topics/images/renditions.md#L6)

**Bounded interpretation:** Renditions are derived image files looked up using transformation and source-related identity; producing one does not replace the original image.

**Challenge:** Request the same rendition twice, then change a focal point or filter; check reuse and distinct derived output.

**Screening reason:** Derived-artifact lifecycle; exact cache identity comes from code evidence, not invented rationale.

**Implementation anchors:** [wagtail/images/models.py:533](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/images/models.py#L533), [wagtail/images/models.py:569](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/images/models.py#L569)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W17 — Changing the custom image model after deployment

**Disposition:** advance · **Family:** wagtail/image-model-migration

**Reference:** [W17: docs/advanced_topics/images/custom_image_model.md:66](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/advanced_topics/images/custom_image_model.md#L66)

**Bounded interpretation:** Selecting a model in configuration does not by itself migrate existing image and rendition data.

**Challenge:** Switch the setting with existing content and distinguish model resolution from a safe data migration.

**Screening reason:** Explicit migration reference located and model-resolution code inspected. Configuration switches resolution but does not copy old data; a migration fixture is still required.

**Implementation anchors:** [wagtail/images/__init__.py:5](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/images/__init__.py#L5)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W18 — Permission-policy internals do not carry public API guarantees

**Disposition:** control · **Family:** wagtail/api-authority

**Reference:** [W18: docs/reference/permissions.md:8](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/reference/permissions.md#L8)

**Bounded interpretation:** Importability and registry usage do not establish the hidden support guarantee; retain the documented public-function exception only in the documents-visible condition.

**Challenge:** A convenient internal policy API is selected for a long-lived extension; require authority before promising compatibility.

**Screening reason:** Authority-negative control; code cannot establish future support commitments.

**Implementation anchors:** [wagtail/permissions.py:12](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/permissions.py#L12)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W19 — Admin access is restricted to trusted users

**Disposition:** control · **Family:** wagtail/trust-authority

**Reference:** [W19: docs/topics/permissions.md:10](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/topics/permissions.md#L10)

**Bounded interpretation:** Fine-grained editor permissions do not establish that arbitrary untrusted users are within the project's intended admin threat model.

**Challenge:** A deployment proposes open public editor accounts; code-only answer cannot certify the intended trust assumption.

**Screening reason:** Organisational trust statement, not an inferable authorization rule.

**Implementation anchors:** [wagtail/admin/auth.py:103](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/admin/auth.py#L103)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W20 — Patch compatibility has a security/data-loss exception

**Disposition:** control · **Family:** wagtail/release-authority

**Reference:** [W20: docs/releases/release_process.md:16](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/releases/release_process.md#L16)

**Bounded interpretation:** A version tuple cannot establish the published future compatibility promise or its exceptions.

**Challenge:** A patch release changes behavior to address data loss; hidden release policy must not be guessed as established authority.

**Screening reason:** Authority-negative control, with a version file as evidence context rather than proof of policy.

**Implementation anchors:** [wagtail/__init__.py:9](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/wagtail/__init__.py#L9)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### W21 — Four-space indentation

**Disposition:** reject · **Family:** wagtail/formatting

**Reference:** [W21: docs/contributing/python_guidelines.md:9](https://github.com/wagtail/wagtail/blob/bddc5eaf2e77d6777b11d0e8cd4a3b62cf707417/docs/contributing/python_guidelines.md#L9)

**Bounded interpretation:** The project specifies four-space indentation.

**Challenge:** A differently indented otherwise equivalent file.

**Screening reason:** Formatting compliance is outside the main interpretation claim; rejected rather than used to inflate sample size.

## paperless-ngx

### P01 — Watcher and task processor have separate responsibilities

**Disposition:** advance · **Family:** paperless-ngx/consumption-pipeline

**Reference:** [P01: docs/usage.md:1164](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L1164)

**Bounded interpretation:** The directory watcher submits consumption work; workers perform document processing, also accepting other ingestion sources.

**Challenge:** A slow parser should occupy worker processing rather than block the watcher from discovering all later files.

**Screening reason:** Architectural request/discovery/worker boundary; transport and concurrency fixture still needed.

**Implementation anchors:** [src/documents/management/commands/document_consumer.py:312](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/management/commands/document_consumer.py#L312), [src/documents/tasks.py:182](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/tasks.py#L182)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P02 — Pre-consumption mutations use a working copy

**Disposition:** advance · **Family:** paperless-ngx/consumption-hooks

**Reference:** [P02: docs/advanced_usage.md:217](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/advanced_usage.md#L217)

**Bounded interpretation:** The pre-hook receives original and working paths; a modifying hook should use the working copy rather than retrigger the watched source.

**Challenge:** A deterministic modification of the working copy versus editing the watched original.

**Screening reason:** File ownership and processing-stage boundary; do not infer all external hooks are safe.

**Implementation anchors:** [src/documents/consumer.py:290](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/consumer.py#L290), [src/documents/consumer.py:312](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/consumer.py#L312)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P03 — Post-consumption hook runs after successful storage

**Disposition:** advance · **Family:** paperless-ngx/consumption-hooks

**Reference:** [P03: docs/advanced_usage.md:288](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/advanced_usage.md#L288)

**Bounded interpretation:** A post-hook runs after the core consumption/storage phase and is not a rollback mechanism for that completed phase.

**Challenge:** A failing post-hook versus a failure inside transactional storage; distinguish recorded task failure from reversal of stored data.

**Screening reason:** Lifecycle and transaction boundary; filesystem and database effects need separate checks.

**Implementation anchors:** [src/documents/consumer.py:332](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/consumer.py#L332), [src/documents/consumer.py:793](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/consumer.py#L793)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P04 — Duplicate handling is conditional at this snapshot

**Disposition:** advance · **Family:** paperless-ngx/duplicate-consumption

**Reference:** [P04: docs/configuration.md:1361](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/configuration.md#L1361)

**Bounded interpretation:** Matching original or archive hashes causes duplicate rejection/deletion only when the configured duplicate-deletion mode is enabled; duplicates are otherwise allowed at this snapshot.

**Challenge:** Identical content under the two settings, including a match in trash; do not reuse older reject-all assumptions.

**Screening reason:** Version-sensitive lifecycle rule; exact default is easy but the combined behavior is substantive.

**Implementation anchors:** [src/documents/consumer.py:1003](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/consumer.py#L1003), [src/paperless/settings/__init__.py:824](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/paperless/settings/__init__.py#L824)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P05 — Workflow assignments override scalars and merge sets

**Disposition:** advance · **Family:** paperless-ngx/workflow-processing

**Reference:** [P05: docs/usage.md:485](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L485)

**Bounded interpretation:** Actions run in order; later scalar assignments override while multi-item assignments such as tags are merged unless an explicit removal action applies.

**Challenge:** Two ordered actions set conflicting correspondent values and overlapping tag sets.

**Screening reason:** Noncommutative action composition with legitimate removal exceptions.

**Implementation anchors:** [src/documents/signals/handlers.py:926](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/signals/handlers.py#L926), [src/documents/workflows/mutations.py:16](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/workflows/mutations.py#L16), [src/documents/workflows/utils.py:14](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/workflows/utils.py#L14)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P06 — Workflow filters depend on processing stage

**Disposition:** advance · **Family:** paperless-ngx/workflow-processing

**Reference:** [P06: docs/usage.md:497](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L497)

**Bounded interpretation:** Consumption-started filters can use source context; added/updated stages use extracted document metadata and content under their supported filter rules.

**Challenge:** A filename/source filter before consumption versus a content filter after extraction.

**Screening reason:** Pipeline information availability; related to P05, not another independent subsystem.

**Implementation anchors:** [src/documents/signals/handlers.py:806](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/signals/handlers.py#L806), [src/documents/matching.py:637](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/matching.py#L637)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P07 — Global access and object permissions both matter

**Disposition:** advance · **Family:** paperless-ngx/object-permissions

**Reference:** [P07: docs/usage.md:426](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L426)

**Bounded interpretation:** Access to an endpoint does not automatically authorize every object returned by that endpoint; queryset and object checks must respect ownership and grants.

**Challenge:** A user with document-view capability requests a document owned by someone else without an object grant.

**Screening reason:** Crosses endpoint authorization and data selection.

**Implementation anchors:** [src/documents/permissions.py:30](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/permissions.py#L30), [src/documents/permissions.py:267](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/permissions.py#L267)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P08 — Ownerless objects are a compatibility exception

**Disposition:** advance · **Family:** paperless-ngx/object-permissions

**Reference:** [P08: docs/usage.md:456](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L456)

**Bounded interpretation:** Ownerless objects are treated differently from privately owned objects; this exception does not mean anonymous endpoint access is permitted.

**Challenge:** Ownerless and privately owned documents under the same authenticated endpoint permissions.

**Screening reason:** Important exception within P07's family; historical compatibility rationale is only documented evidence.

**Implementation anchors:** [src/documents/permissions.py:455](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/permissions.py#L455), [src/documents/permissions.py:176](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/permissions.py#L176)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P09 — Workflow configuration is global rather than owner-scoped

**Disposition:** advance · **Family:** paperless-ngx/workflow-authority

**Reference:** [P09: docs/usage.md:753](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L753)

**Bounded interpretation:** Workflow definitions are shared and governed by application-level permissions, rather than an owner-specific workflow collection.

**Challenge:** Two users with workflow-edit permission see the same workflows; do not infer workflows inherit document ownership restrictions.

**Screening reason:** Administrative boundary with potential effects on many documents.

**Implementation anchors:** [src/documents/models.py:1967](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/models.py#L1967), [src/documents/views.py:5009](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/views.py#L5009)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P10 — Classifier training excludes inbox material

**Disposition:** advance · **Family:** paperless-ngx/classifier-training

**Reference:** [P10: docs/advanced_usage.md:76](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/advanced_usage.md#L76)

**Bounded interpretation:** The training corpus excludes documents carrying an inbox tag; removing that tag can make a labelled document eligible for training.

**Challenge:** A document with both an inbox tag and a topical tag versus one whose inbox tag has been removed.

**Screening reason:** Data-selection boundary; code cannot prove the remaining labels are actually correct.

**Implementation anchors:** [src/documents/classifier.py:224](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/classifier.py#L224), [src/documents/classifier.py:233](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/classifier.py#L233)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P11 — Persistent filenames require coordinated moves

**Disposition:** advance · **Family:** paperless-ngx/file-identity

**Reference:** [P11: docs/advanced_usage.md:377](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/advanced_usage.md#L377)

**Bounded interpretation:** Stored file names are part of document state; changing physical paths requires coordinated updates rather than an untracked filesystem move.

**Challenge:** A metadata/storage-path rename through the application versus moving the file externally.

**Screening reason:** Database/filesystem consistency; changing the global format requires an explicit existing-file rename step.

**Implementation anchors:** [src/documents/file_handling.py:65](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/file_handling.py#L65), [src/documents/management/commands/document_renamer.py:7](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/management/commands/document_renamer.py#L7)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P12 — Trash and permanent deletion are different states

**Disposition:** defer · **Family:** paperless-ngx/document-deletion

**Reference:** [P12: docs/usage.md:816](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L816)

**Bounded interpretation:** Soft deletion preserves recoverable state; final deletion removes database/archive state, and an optional trash destination retains only the original file.

**Challenge:** Restore a soft-deleted document versus recover from the configured post-deletion directory.

**Screening reason:** Permanent cleanup is visible locally, but the soft-delete manager/restore semantics come from django-softdelete. Pin and inspect that dependency before final lifecycle gold.

**Implementation anchors:** [src/documents/models.py:513](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/models.py#L513), [src/documents/tasks.py:471](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/tasks.py#L471), [src/documents/signals/handlers.py:344](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/signals/handlers.py#L344)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P13 — Archive-generation settings have parser-specific exceptions

**Disposition:** advance · **Family:** paperless-ngx/archive-rendition

**Reference:** [P13: docs/configuration.md:964](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/configuration.md#L964)

**Bounded interpretation:** Archive policy depends on mode, document characteristics, and parser rendition requirements; never mode does not remove a mandatory display rendition.

**Challenge:** A scanned image, born-digital PDF, and a format requiring a PDF rendition under the same mode.

**Screening reason:** Conditional behavior across orchestration and parser capability.

**Implementation anchors:** [src/documents/consumer.py:124](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/consumer.py#L124), [src/paperless/parsers/tika.py:63](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/paperless/parsers/tika.py#L63)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P14 — PDF editing documentation omits the inspected versioning path

**Disposition:** control · **Family:** paperless-ngx/pdf-versioning-conflict

**Reference:** [P14: docs/usage.md:806](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L806)

**Bounded interpretation:** The guide describes editing the original, but the inspected rotate/delete-pages paths write a temporary PDF and enqueue consumption with a root_document_id to create a new version. Do not claim in-place byte mutation or guaranteed archival retention without tracing the version pipeline.

**Challenge:** Documents-visible interpretation must reconcile original-file wording with new-version dispatch; code-only should describe that dispatch. A fixture must inspect old and new bytes after worker completion.

**Screening reason:** Concrete source/documentation mismatch found during deeper review. Full retention semantics have not been executed, so this is a conflict candidate rather than a proven immutable-original guarantee.

**Implementation anchors:** [src/documents/bulk_edit.py:446](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/bulk_edit.py#L446), [src/documents/bulk_edit.py:814](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/bulk_edit.py#L814)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P15 — Parser plugins use a structural interface and entry points

**Disposition:** advance · **Family:** paperless-ngx/parser-extension

**Reference:** [P15: docs/development.md:408](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/development.md#L408)

**Bounded interpretation:** A parser can satisfy the protocol without inheriting a prescribed base class; discovery uses package entry points and validates required class-level members.

**Challenge:** A structurally valid external parser with no inheritance versus a subclass missing a required member.

**Screening reason:** Extension boundary connecting discovery and interface validation.

**Implementation anchors:** [src/paperless/parsers/__init__.py:117](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/paperless/parsers/__init__.py#L117), [src/paperless/parsers/registry.py:216](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/paperless/parsers/registry.py#L216)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P16 — Parser selection uses scores, abstention, and tie precedence

**Disposition:** advance · **Family:** paperless-ngx/parser-extension

**Reference:** [P16: docs/development.md:442](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/development.md#L442)

**Bounded interpretation:** Eligible parsers compete by score; None declines, and equal scores prefer external parsers through evaluation order.

**Challenge:** Higher-scored built-in, tied external parser, and an external parser returning None.

**Screening reason:** Selection and extension interaction; correlated with P15.

**Implementation anchors:** [src/paperless/parsers/registry.py:332](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/paperless/parsers/registry.py#L332), [src/paperless/parsers/registry.py:380](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/paperless/parsers/registry.py#L380)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P17 — Remote parser eligibility depends on declared capability

**Disposition:** advance · **Family:** paperless-ngx/parser-remote-boundary

**Reference:** [P17: docs/development.md:474](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/development.md#L474)

**Bounded interpretation:** Declared remote parsers are excluded when remote processing is not allowed; an undeclared third-party remote call is not prevented by this metadata gate.

**Challenge:** A declared remote parser outranks a local one while remote processing is disabled; contrast an undeclared remote implementation.

**Screening reason:** Capability gate with an important trust limitation; does not prove network confinement.

**Implementation anchors:** [src/paperless/parsers/registry.py:365](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/paperless/parsers/registry.py#L365), [src/documents/consumer.py:458](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/consumer.py#L458)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P18 — External database modifications require downtime

**Disposition:** control · **Family:** paperless-ngx/database-operations-authority

**Reference:** [P18: docs/configuration.md:258](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/configuration.md#L258)

**Bounded interpretation:** The code/configuration does not establish authorization for live external database edits; the operational prohibition requires its published policy reference.

**Challenge:** An operator proposes restoring or manually modifying the database while workers run.

**Screening reason:** Authority-negative control; code can identify consistency risks but cannot establish the hidden operational rule as approved.

**Implementation anchors:** [src/paperless/settings/__init__.py:544](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/paperless/settings/__init__.py#L544)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P19 — Audit log actor differs for workflow changes

**Disposition:** defer · **Family:** paperless-ngx/audit-trail

**Reference:** [P19: docs/usage.md:812](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L812)

**Bounded interpretation:** The published history behavior distinguishes system/workflow changes from attributed user changes; audit completeness depends on enabled settings and paths.

**Challenge:** A manual metadata edit versus a workflow edit with audit logging enabled.

**Screening reason:** Reference located, but exact audit-actor integration not traced sufficiently. Do not use this as calibrated gold until that path is inspected and exercised.

**Implementation anchors:** [src/documents/signals/handlers.py:806](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/documents/signals/handlers.py#L806)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### P20 — Parser identity must exist before instantiation

**Disposition:** merge · **Family:** paperless-ngx/parser-extension

**Reference:** [P20: docs/development.md:414](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/development.md#L414)

**Bounded interpretation:** Discovery reads parser identity and required methods on the class, before creating a parser instance.

**Challenge:** Move identity fields into the instance constructor.

**Screening reason:** Merge into P15 as a negative challenge instead of inflating the decision count.

**Implementation anchors:** [src/paperless/parsers/registry.py:56](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/src/paperless/parsers/registry.py#L56)

### P21 — Keyboard shortcut help

**Disposition:** reject · **Family:** paperless-ngx/interface-help

**Reference:** [P21: docs/usage.md:1020](https://github.com/paperless-ngx/paperless-ngx/blob/835c4e51d0b145007bfac934009713dd8bbf3598/docs/usage.md#L1020)

**Bounded interpretation:** The application exposes shortcut help.

**Challenge:** Open the shortcut-help interface.

**Screening reason:** User-interface feature lookup offers no meaningful architectural interpretation challenge; no implementation audit warranted.

## httpx

### H01 — Client lifetime owns reusable transport resources

**Disposition:** advance · **Family:** httpx/client-lifetime

**Reference:** [H01: docs/advanced/clients.md:13](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/clients.md#L13)

**Bounded interpretation:** A reused client owns a persistent transport/pool and should be closed at the end of its lifetime; top-level requests create shorter-lived clients.

**Challenge:** A batch of requests through one client versus constructing a client per request; check ownership and close behavior without claiming a measured speedup.

**Screening reason:** Resource lifecycle spans top-level API, client, and transport; actual connection reuse depends on httpcore.

**Implementation anchors:** [httpx/_api.py:102](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_api.py#L102), [httpx/_client.py:156](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L156), [httpx/_transports/default.py:156](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_transports/default.py#L156)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H02 — Client and request configuration merge selectively

**Disposition:** advance · **Family:** httpx/request-configuration

**Reference:** [H02: docs/advanced/clients.md:96](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/clients.md#L96)

**Bounded interpretation:** Building a request merges selected collections, with request values overriding conflicts; other supported options follow their own override semantics.

**Challenge:** Shared client headers and per-request overrides while preserving unrelated headers and parameters.

**Screening reason:** Configuration composition; do not infer every client option is available per request.

**Implementation anchors:** [httpx/_client.py:340](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L340), [httpx/_client.py:424](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L424), [httpx/_client.py:433](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L433)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H03 — Explicit requests bypass automatic client-option merging

**Disposition:** advance · **Family:** httpx/request-configuration

**Reference:** [H03: docs/advanced/clients.md:162](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/clients.md#L162)

**Bounded interpretation:** Build_request applies client configuration before sending; a directly constructed Request is not retroactively given all client headers and base-URL configuration by send.

**Challenge:** Remove a sensitive header after build_request, and compare send of a directly constructed Request.

**Screening reason:** Preparation/dispatch boundary; grouped with H02.

**Implementation anchors:** [httpx/_client.py:340](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L340), [httpx/_client.py:879](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L879)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H04 — Streaming response ownership requires closure

**Disposition:** advance · **Family:** httpx/response-lifetime

**Reference:** [H04: docs/async.md:87](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/async.md#L87)

**Bounded interpretation:** Context-managed streaming closes the response on exit; manual streaming transfers responsibility for eventual closure to the caller.

**Challenge:** Partially consume a response then exit normally or raise; contrast manual send with explicit close.

**Screening reason:** Resource ownership and exceptional control flow.

**Implementation anchors:** [httpx/_client.py:1543](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L1543), [httpx/_client.py:1594](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L1594), [httpx/_models.py:1065](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_models.py#L1065)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H05 — Response hooks precede automatic body consumption

**Disposition:** advance · **Family:** httpx/response-lifetime

**Reference:** [H05: docs/advanced/event-hooks.md:34](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/event-hooks.md#L34)

**Bounded interpretation:** Response hooks run before the client decides to read the body; a hook needing bytes must read explicitly, using the appropriate sync/async API.

**Challenge:** A streaming response hook accesses content before read versus an explicitly reading hook.

**Screening reason:** Ordering and I/O boundary, not merely registration syntax.

**Implementation anchors:** [httpx/_client.py:964](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L964), [httpx/_client.py:879](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L879)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H06 — Shared authentication logic is separated from sync/async I/O

**Disposition:** advance · **Family:** httpx/authentication-flow

**Reference:** [H06: docs/advanced/authentication.md:125](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/authentication.md#L125)

**Bounded interpretation:** A common generator-based auth flow can serve sync and async clients; body requirements are declared, while other I/O needs the appropriate specialized flow override.

**Challenge:** Add an authentication cache or body-dependent signature without silently blocking the async path.

**Screening reason:** Meaningful interface/side-effect separation with valid alternatives.

**Implementation anchors:** [httpx/_auth.py:62](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_auth.py#L62), [httpx/_auth.py:87](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_auth.py#L87), [httpx/_client.py:930](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L930)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H07 — Transport mounts resolve specific patterns before broad ones

**Disposition:** advance · **Family:** httpx/transport-routing

**Reference:** [H07: docs/advanced/transports.md:338](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/transports.md#L338)

**Bounded interpretation:** Mount resolution uses URL-pattern specificity rather than insertion order; a None exclusion falls back to the ordinary transport.

**Challenge:** Overlapping scheme, domain, and port routes plus an explicit exclusion.

**Screening reason:** Routing and precedence cross implementation components.

**Implementation anchors:** [httpx/_utils.py:206](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_utils.py#L206), [httpx/_client.py:760](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L760)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H08 — Extensions carry optional transport information

**Disposition:** advance · **Family:** httpx/transport-interface

**Reference:** [H08: docs/advanced/extensions.md:5](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/extensions.md#L5)

**Bounded interpretation:** Request extensions carry optional metadata such as timeouts through the client/transport boundary; support for arbitrary extensions is transport-dependent.

**Challenge:** A custom transport forwards a timeout extension while an unknown extension is not assumed implemented.

**Screening reason:** Interface extensibility; inspect upstream dependencies for end-to-end semantics.

**Implementation anchors:** [httpx/_client.py:584](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L584), [httpx/_transports/default.py:247](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_transports/default.py#L247)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H09 — Built-in connection retries do not cover all failure types

**Disposition:** defer · **Family:** httpx/transport-retries

**Reference:** [H09: docs/advanced/transports.md:17](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/transports.md#L17)

**Bounded interpretation:** The documented retries option concerns connection failures, not blanket retries for read errors or HTTP status codes.

**Challenge:** ConnectError versus a 503 response and a read failure under the same retries setting.

**Screening reason:** Retry implementation is in httpcore; pin and inspect it before treating local forwarding code as sufficient gold.

**Implementation anchors:** [httpx/_transports/default.py:165](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_transports/default.py#L165)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H10 — ASGI request transport excludes application lifespan management

**Disposition:** advance · **Family:** httpx/transport-interface

**Reference:** [H10: docs/advanced/transports.md:145](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/transports.md#L145)

**Bounded interpretation:** The ASGI transport dispatches HTTP scopes and does not provide startup/shutdown lifespan orchestration; that lifecycle requires a separate component.

**Challenge:** An application requiring startup state under bare transport versus an external lifespan manager.

**Screening reason:** Explicit responsibility boundary with a plausible but wrong expectation.

**Implementation anchors:** [httpx/_transports/asgi.py:99](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_transports/asgi.py#L99), [httpx/_transports/asgi.py:107](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_transports/asgi.py#L107)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H11 — Per-request cookie documentation overstates removal

**Disposition:** control · **Family:** httpx/cookie-policy

**Reference:** [H11: docs/compatibility.md:114](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/compatibility.md#L114)

**Bounded interpretation:** At this snapshot per-request client cookies still work with a deprecation warning; recommended client-level storage is distinct from an enforced ban.

**Challenge:** Give documents and code together and require a discrepancy report; code-only must not invent hidden removal policy.

**Screening reason:** Concrete documentation/code conflict; do not use the documentation alone as an answer key.

**Implementation anchors:** [httpx/_client.py:806](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L806), [httpx/_client.py:413](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L413)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H12 — Response-encoding documentation conflicts with default behavior

**Disposition:** control · **Family:** httpx/encoding-policy

**Reference:** [H12: docs/compatibility.md:101](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/compatibility.md#L101)

**Bounded interpretation:** The default response fallback is UTF-8 unless overridden; the compatibility guide's automatic charset-detection description conflicts with the dedicated guide and implementation.

**Challenge:** A no-charset response under default settings versus a configured detection callable.

**Screening reason:** Conflict control with executable discriminator; hidden-document conflict is scored only when documents are visible.

**Implementation anchors:** [httpx/_models.py:167](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_models.py#L167), [httpx/_client.py:202](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L202)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H13 — Redirect default does not reveal its design motivation

**Disposition:** control · **Family:** httpx/redirect-authority

**Reference:** [H13: docs/compatibility.md:12](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/compatibility.md#L12)

**Bounded interpretation:** Code supports the default and opt-in behavior; it does not establish the published motivation about visibility of network calls as the actual reason.

**Challenge:** Recover the default but ask separately for motive; accept unconfirmed rationale rather than fabricated certainty.

**Screening reason:** Useful content-versus-intent control; do not count the same default twice as positive evidence.

**Implementation anchors:** [httpx/_client.py:197](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L197), [httpx/_client.py:964](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L964)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H14 — Timeout default is a local parameter fact

**Disposition:** calibration · **Family:** httpx/timeout-default

**Reference:** [H14: docs/advanced/timeouts.md:3](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/timeouts.md#L3)

**Bounded interpretation:** Default network inactivity timeout is five seconds, with explicit disabling and phase-specific settings available.

**Challenge:** Distinguish a default inactivity timeout from a total wall-clock deadline.

**Screening reason:** Local/default recovery is calibration; phase enforcement belongs to the transport dependency.

**Implementation anchors:** [httpx/_config.py:246](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_config.py#L246)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H15 — SSL configuration belongs to client transport construction

**Disposition:** advance · **Family:** httpx/client-lifetime

**Reference:** [H15: docs/compatibility.md:174](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/compatibility.md#L174)

**Bounded interpretation:** SSL configuration initializes transport resources at client construction; different SSL configurations require appropriately separate clients/transports rather than arbitrary per-request verify settings.

**Challenge:** Requests to two trust domains with different SSL contexts; reject adding an unsupported request-level option.

**Screening reason:** Configuration follows resource ownership; related to H01 rather than independent repetition.

**Implementation anchors:** [httpx/_client.py:718](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L718), [httpx/_transports/default.py:153](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_transports/default.py#L153)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H16 — Multipart file uploads require binary streams

**Disposition:** calibration · **Family:** httpx/multipart-input

**Reference:** [H16: docs/compatibility.md:94](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/compatibility.md#L94)

**Bounded interpretation:** Multipart uploads reject text-mode file objects; binary streams preserve bytes.

**Challenge:** Equivalent text-mode and binary-mode file objects.

**Screening reason:** A direct local validation check; insufficient architectural depth for headline evidence.

**Implementation anchors:** [httpx/_multipart.py:162](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_multipart.py#L162)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H17 — HTTP/2 opt-in does not prove the published robustness rationale

**Disposition:** control · **Family:** httpx/http2-authority

**Reference:** [H17: docs/http2.md:22](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/http2.md#L22)

**Bounded interpretation:** The default HTTP/2 setting is observable; the project rationale about comparative maturity cannot be established from a Boolean or the presence of two implementations.

**Challenge:** Distinguish available protocol support from an empirically proven reliability ranking.

**Screening reason:** Authority/rationale-negative control; no performance or reliability result is implied.

**Implementation anchors:** [httpx/_client.py:650](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L650), [httpx/_transports/default.py:162](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_transports/default.py#L162)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H18 — Sync and async request streams must match dispatch

**Disposition:** advance · **Family:** httpx/stream-interface

**Reference:** [H18: docs/async.md:109](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/async.md#L109)

**Bounded interpretation:** Client dispatch and transport consume their matching stream interfaces; async streaming request bodies cannot be supplied as ordinary sync iterators interchangeably.

**Challenge:** Feed a sync generator to async dispatch versus an async generator, preserving streaming rather than prebuffering everything.

**Screening reason:** Crosses encoding, client, and transport contracts.

**Implementation anchors:** [httpx/_client.py:1001](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L1001), [httpx/_client.py:1717](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L1717), [httpx/_content.py:67](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_content.py#L67)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H19 — No-proxy routes are mount exclusions

**Disposition:** merge · **Family:** httpx/transport-routing

**Reference:** [H19: docs/advanced/transports.md:417](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/advanced/transports.md#L417)

**Bounded interpretation:** No-proxy routes use specific exclusions and ordinary transport fallback.

**Challenge:** A broad proxy route with one excluded domain.

**Screening reason:** Merge into H07; a second wording of the same precedence mechanism is not an independent decision.

**Implementation anchors:** [httpx/_client.py:760](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L760), [httpx/_utils.py:30](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_utils.py#L30)

### H20 — Bodyless convenience methods retain a generic escape hatch

**Disposition:** calibration · **Family:** httpx/request-method-api

**Reference:** [H20: docs/compatibility.md:182](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/compatibility.md#L182)

**Bounded interpretation:** Convenience methods omit body parameters, while the generic request API permits explicit bodies for those methods.

**Challenge:** A body passed to get versus request with method GET; do not turn convenience API design into a universal protocol prohibition.

**Screening reason:** Useful exception calibration; the guide's broad protocol explanation is not adopted as external HTTP truth.

**Implementation anchors:** [httpx/_client.py:1036](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L1036), [httpx/_client.py:771](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/httpx/_client.py#L771)

**Remaining work:** semantic disclosure review, gold/evaluator review, and runnable fixture validation. No counterfactual variant has been built.

### H21 — Uppercase status-code naming preference

**Disposition:** reject · **Family:** httpx/naming-style

**Reference:** [H21: docs/compatibility.md:125](https://github.com/encode/httpx/blob/b5addb64f0161ff6bfe94c124ef76f6a1fba5254/docs/compatibility.md#L125)

**Bounded interpretation:** The documentation prefers uppercase status names while retaining lowercase compatibility.

**Challenge:** Use equivalent uppercase/lowercase names.

**Screening reason:** A naming preference is not a substantive decision-family test; reject from the main set.
