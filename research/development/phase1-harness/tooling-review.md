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

For now, the only implemented transport is a trusted scripted worker. Supplying a live transport is rejected. A disabled model path prevents accidental spending here but does not constitute an implemented or qualified model gateway.
