import type { Metadata } from 'next';
import { Shell } from '../ui';
import { PhaseRoadmap } from './phase-roadmap';

export const dynamic = 'force-static';
export const metadata: Metadata = {title:'Study roadmap',description:'A first credible trial, a separate confirmation and possible later studies of broader use.'};
export default function PhasesPage(){return <Shell active="phases"><PhaseRoadmap/></Shell>}
