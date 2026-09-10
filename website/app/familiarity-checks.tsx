export function FamiliarityChecks() {
  return <>
    <p>Asking a model whether it recognises a project is not enough. The experiment will look for observable recall in two separate checks, at the relevant selection stage. Repository checks belong to Phase 1; historical fix reconstruction belongs to selecting coding tasks for Phase 2.</p>
    <ol className="plain-list">
      <li><strong>When screening repositories:</strong> give the model a short excerpt with a distinctive detail removed, such as unusual comment wording or an arbitrary test value. Ask it to recover the missing detail. Include comparable, newly written snippets to see how often it can guess without prior exposure.</li>
      <li><strong>When selecting historical tasks:</strong> give the model a limited task description, with no repository access, and ask where and how it would make the change. Compare the answer with distinctive details of the historical fix that were not supplied in the prompt.</li>
    </ol>
    <p>A conventional correct solution could come from reasoning. Reproducing unusual details is more suggestive of recall. Neither test can prove that the model has never seen the material.</p>
    <p>We will set the questions, scoring rules and number of attempts before running these checks. We will use the exact model versions intended for the experiment.</p><p>Each check runs in a separate session. The model can read only the supplied excerpt or task description, with no browsing or additional file access. Its questions and answers will stay out of the later experimental agents’ histories.</p>
    <p>We will run these checks when choosing repositories and tasks, rather than during every coding attempt. We will revisit them if the model version or selected material changes.</p><p>The report will keep all outcomes, including unsuccessful attempts. It will say “familiarity detected” or “not detected by these probes”. It will never describe a lack of detected recall as proof that the material was unfamiliar.</p><p>Evidence of familiarity will inform whether we use a repository and how we interpret its results. It will not automatically exclude the repository. We will record the selection decision and its reason.</p>
    <p>The test of missing details adapts <a className="text-link" href="https://arxiv.org/abs/2311.09783" target="_blank" rel="noreferrer">research on recovering omitted benchmark details</a>. It still needs a protocol suited to these repositories. Removing project names is an optional diagnostic, not proof that code is unfamiliar.</p>
  </>;
}
