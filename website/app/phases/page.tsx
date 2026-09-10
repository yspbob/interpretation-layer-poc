import type { Metadata } from 'next';
import { Shell } from '../ui';
import { PhaseRoadmap } from './phase-roadmap';

export const dynamic = 'force-static';
export const metadata: Metadata = {title:'First trial roadmap',description:'Three parts of the first trial: reconstruct guidance, test its use, then test interaction during work.'};
export default function PhasesPage(){return <Shell active="phases"><PhaseRoadmap/></Shell>}
