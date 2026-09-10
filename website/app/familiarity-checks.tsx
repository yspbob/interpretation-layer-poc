export function FamiliarityChecks() {
  return <>
    <p>Asking a model whether it recognises a project is not enough. The experiment will look for observable recall in two separate checks, before using the selected model and cases in the pilot.</p>
    <ol className="plain-list">
      <li><strong>When screening repositories:</strong> give the model a short excerpt with a distinctive detail removed, such as unusual comment wording or an arbitrary test value. Ask it to recover the missing detail. Include comparable, newly written snippets to see how often it can guess without prior exposure.</li>
      <li><strong>When selecting historical tasks:</strong> give the model a limited task description, with no repository access, and ask where and how it would make the change. Compare the answer with distinctive details of the historical fix that were not supplied in the prompt.</li>
    </ol>
    <p>A conventional correct solution could come from reasoning. Reproducing unusual details is more suggestive of recall. Neither test can prove that the model has never seen the material.</p>
    <p>The prompts, scoring rules and number of attempts are set in advance. Probes use the exact model versions intended for the relevant roles, in separate sessions without browsing or file access beyond the supplied excerpts. Their questions and answers never enter the experimental agents’ histories.</p>
    <p>These checks are not repeated during every coding run. They are revisited if the model version or selected material changes. Reports retain unsuccessful probes and any selection decisions, using “familiarity detected” or “not detected by these probes”. A positive result informs selection and interpretation; it does not automatically exclude a repository.</p>
    <p>The missing-detail test adapts <a className="text-link" href="https://arxiv.org/abs/2311.09783" target="_blank" rel="noreferrer">research on recovering omitted benchmark details</a>. It still needs a protocol suited to these repositories. Removing project names is an optional diagnostic, not proof that code is unfamiliar.</p>
  </>;
}
