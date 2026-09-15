"""Public synthetic failure checks. No model calls or qualification labels."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from fable_direct import audit, prepare, verify, sha, WORKER, MODEL, VERSION, check_input
from prepare_fable_qualification import render, prepare as prepare_desktop
from qualification_batch import load_bank
from test_qualification_batch import synthetic_bank, synthetic_answer


class DirectTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        freeze=synthetic_bank(self.root/'bank')
        self.bank=load_bank(self.root/'bank','freeze.json',freeze)
        self.item=next(i for i in self.bank.items.values() if i['role']=='guidance_assessor')
        self.raw=render(self.item)
        self.rows=[{'type':'user','version':VERSION,'message':{'content':self.raw.decode()}},
            {'type':'attachment','attachment':{'type':'prompt_snapshot','systemPrompt':[WORKER['worker']['prompt']],'tools':[]}},
            {'type':'assistant','version':VERSION,'effort':'high','perTurnEffort':'high','requestId':'req-public',
             'message':{'id':'msg-public','model':MODEL,'usage':{'iterations':[{'type':'message'}]},
                        'content':[{'type':'text','text':json.dumps(synthetic_answer(self.item['packet']))}]}}]
        self.addCleanup(patch.stopall)
        patch('socket.socket.connect',side_effect=AssertionError('No network')).start()

    def test_valid_record_and_split_stream_message(self):
        self.assertEqual(audit(self.raw,self.rows)['decision'],'structure_pass')
        thinking=deepcopy(self.rows[-1])
        thinking['message']['content']=[{'type':'thinking','thinking':''}]
        self.rows.insert(2,thinking)
        self.assertEqual(audit(self.raw,self.rows)['recorded_messages'],1)
        self.assertEqual(audit(self.raw,self.rows)['decision'],'structure_pass')

    def test_changed_input_and_extra_user_stop(self):
        for mutation in [lambda r:r[0]['message'].update(content=r[0]['message']['content']+' '),
                         lambda r:r.append(deepcopy(r[0]))]:
            rows=deepcopy(self.rows)
            mutation(rows)
            self.assertIn('input_or_context_mismatch',audit(self.raw,rows)['control_errors'])

    def test_model_tools_missing_snapshot_and_continuation_stop(self):
        mutations=[lambda r:r[-1]['message'].update(model='other'),
                   lambda r:r[-1].update(effort='low'),
                   lambda r:r[1]['attachment'].update(tools=[{'name':'Read'}]),
                   lambda r:r.pop(1),
                   lambda r:r[-1]['message']['usage'].update(iterations=[{},{}]),
                   lambda r:r[-1]['message']['content'].append({'type':'tool_use','name':'Read'}),
                   lambda r:r[1]['attachment'].update(systemPrompt=['changed']),
                   lambda r:r[-1].update(version='other')]
        for mutation in mutations:
            rows=deepcopy(self.rows)
            mutation(rows)
            self.assertEqual(audit(self.raw,rows)['decision'],'stop')
        extra=deepcopy(self.rows[-1])
        extra['message']['id']='msg-second'
        extra['requestId']='req-second'
        self.assertEqual(audit(self.raw,self.rows+[extra])['decision'],'stop')

    def test_invalid_answer_preserved_and_not_control_pass(self):
        for value in ['{}','{"candidate_hash":"a","candidate_hash":"b"}', 'not JSON']:
            rows=deepcopy(self.rows)
            rows[-1]['message']['content']=[{'type':'text','text':value}]
            result=audit(self.raw,rows)
            self.assertEqual(result['decision'],'preserve_invalid')
            self.assertEqual(result['raw_answer'],value)

    def test_candidate_schema_and_source_integrity(self):
        for mutation in [lambda i:i['packet']['candidate']['claims'][0].update(kind='invalid'),
                         lambda i:i['packet']['sources']['files']['source.txt'].update(text='changed')]:
            item=deepcopy(self.item)
            mutation(item)
            from harness import digest
            item['packet']['candidate_hash']=digest(item['packet']['candidate'])
            with self.assertRaises(Exception): check_input(render(item))

    def test_freeze_all_inputs_unchanged_and_preserve_existing(self):
        desktop=prepare_desktop(self.bank,self.root/'desktop')
        output=self.root/'direct'
        result=prepare(self.root/'desktop',desktop['desktop_freeze_sha256'],output)
        self.assertEqual(result['input_count'],48)
        for n in range(1,49):
            name=f'inputs/{n:03}/input.txt'
            self.assertEqual((output/name).read_bytes(),(self.root/'desktop'/name).read_bytes())
        with self.assertRaisesRegex(ValueError,'Preserve existing'): prepare(self.root/'desktop',desktop['desktop_freeze_sha256'],output)
        (output/'inputs/001/input.txt').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'Changed frozen'): verify(output,result['freeze_sha256'])


if __name__=='__main__': unittest.main()
