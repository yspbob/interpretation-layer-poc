# Tools considered for the first harness

Reviewed on 11 September 2026. This is a documentation review, not a benchmark or an integration test of these products.

| Tool | Useful capability | Decision for this build |
| --- | --- | --- |
| JSON Schema | Validate structured role records | Use the Python jsonschema library, pinned to 4.26.0. Tested in the controller. |
| Promptfoo | Custom providers and assertions; evaluation of existing outputs | A candidate for later qualification runs and reporting. The study still needs its own exact release and role input rules. |
| LiteLLM | A gateway with usage and budget controls | Consider for the live adapter. Its documented budget enforcement needs a database; the database free mode must not be assumed to enforce a spending ceiling. |
| Portkey | Gateway credentials and budget controls | Another candidate for the live adapter. No service, account or paid run is added in this build. |
| Langfuse | Datasets and experiment records | Consider when real assessments need a comparison interface. Local structured records are sufficient for this rehearsal. |

Relevant primary documentation: [Promptfoo configuration](https://www.promptfoo.dev/docs/configuration/reference/), [custom providers](https://www.promptfoo.dev/docs/providers/custom-api/), [Python assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/python/), [LiteLLM budget controls](https://docs.litellm.ai/docs/proxy/users), [Portkey virtual keys](https://portkey.ai/docs/product/ai-gateway/virtual-keys), and [Langfuse datasets](https://langfuse.com/docs/evaluation/experiments/datasets).

The small custom controller handles what is specific to this study: separate permitted evidence, exact admitted claim versions, bounded revisions, retained failures and assessment after release. This does not mean the reviewed tools cannot support the study. Before implementing a live gateway, compare their adapters against destination restrictions, fail closed spending limits, provider metadata, fresh requests and the ability to keep assessment references out of working roles.

At the time of the 11 September review, the only implemented transport was a trusted scripted worker. Live transports were rejected. The 13 September update below records the subsequent adapter implementation.


## Adapter decision: 13 September 2026

The first connection now uses the official OpenAI Python SDK 3.13.0 and its HTTPX2 transport, pinned to 2.12.0. It supports a single fixed Responses endpoint and one sequential attempt. Using the SDK reuses request construction and HTTP handling without deploying a proxy service. The study controller supplies the role and release rules; a small wrapper enforces destination, request, ledger and stop policy.

LiteLLM and Portkey remain candidates if multiple providers or centrally managed budgets become necessary. The present attempt ledger is not an account wide quota service. Promptfoo and Langfuse remain optional for larger qualification datasets and reporting. No claim is made that these products cannot support the study.

The [adapter record](PROVIDER.md) links the official API documentation, records the limits of the spending control and distinguishes simulated SDK checks from live endpoint or model qualification. Model selection, actual prices and spending authorisation remain open.
