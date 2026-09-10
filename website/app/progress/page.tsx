import type { Metadata } from 'next';
import { Shell } from '../ui';
import { ProgressView } from './progress-view';
export const metadata:Metadata={title:'Progress & findings',description:'Current stage, credibility checks, risks, findings and open decisions in the interpretation layer validation study.'};
export const dynamic = 'force-static';
export default function Progress(){return <Shell active="progress"><ProgressView/></Shell>}
