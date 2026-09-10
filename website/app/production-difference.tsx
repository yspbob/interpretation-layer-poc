export function ProductionDifference({ production, poc, limit }: { production: string; poc: string; limit?: string }) {
  return <aside className="production-difference" aria-label="Production and this POC">
    <div><h4>In production</h4><p>{production}</p></div>
    <div><h4>In this POC</h4><p>{poc}</p></div>
    {limit && <p className="production-limit">{limit}</p>}
  </aside>;
}
