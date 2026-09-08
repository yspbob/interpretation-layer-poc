import ast
import asyncio
import copy
import hashlib
import importlib.metadata
import json
import logging
import sys
import types
import warnings
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
(ROOT/'local-runs').mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'sources/httpx'))
import httpx
assert Path(httpx.__file__).resolve().is_relative_to(ROOT/'sources/httpx')
checks=[]
def check(case,label,condition,observed):
    assert condition,(case,label,observed)
    checks.append(dict(case=case,check=label,passed=True,observed=observed))

with httpx.Client(transport=httpx.MockTransport(lambda request:httpx.Response(200,request=request)),trust_env=False,headers={'X-Shared':'yes'},params={'shared':'yes'}) as client:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        response=client.get('https://example.test',cookies={'probe':'value'})
    check('H11','per-request cookies are accepted with deprecation warning',response.request.headers.get('cookie')=='probe=value' and any(issubclass(w.category,DeprecationWarning) for w in caught),{'cookie_header':response.request.headers.get('cookie'),'warning_types':[w.category.__name__ for w in caught]})
    built=client.build_request('GET','https://example.test',headers={'X-Other':'yes'},params={'other':'yes'})
    check('H02','request preparation combines client and request collections',built.headers['X-Shared']=='yes' and built.headers['X-Other']=='yes' and dict(built.url.params)=={'shared':'yes','other':'yes'}, {'headers_present':list(k for k in built.headers if k.startswith('x-')),'params':dict(built.url.params)})
    response=client.send(httpx.Request('GET','https://example.test'))
    check('H03','send does not restore missing client headers', 'X-Shared' not in response.request.headers, {'shared_header_present':'X-Shared' in response.request.headers})

response=httpx.Response(200,content=b'\xe9'*64)
check('H12','default no-charset response encoding is UTF-8',response.encoding=='utf-8',{'encoding':response.encoding})
response=httpx.Response(200,content=b'\xe9'*64,default_encoding=lambda b:'latin-1')
check('H12','detection callable is an explicit alternative',response.encoding=='latin-1' and response.text=='é'*64,{'encoding':response.encoding})

class ProbeStream(httpx.SyncByteStream):
    closed=False
    def __iter__(self):yield b'first';yield b'second'
    def close(self):self.closed=True
stream=ProbeStream();hook_saw_unread=[]
def hook(response):
    try:response.content;hook_saw_unread.append(False)
    except httpx.ResponseNotRead:hook_saw_unread.append(True)
with httpx.Client(transport=httpx.MockTransport(lambda request:httpx.Response(200,stream=stream)),event_hooks={'response':[hook]},trust_env=False) as client:
    with client.stream('GET','https://example.test') as response:next(response.iter_bytes())
check('H04','stream context closes a partly consumed response',stream.closed,{'closed':stream.closed})
check('H05','response hook executes before body is read',hook_saw_unread==[True],{'hook_saw_unread':hook_saw_unread})

def transport(label):return httpx.MockTransport(lambda request:httpx.Response(200,text=label))
with httpx.Client(transport=transport('ordinary'),mounts={'all://':transport('broad'),'https://example.test:8443':transport('port'),'all://excluded.test':None},trust_env=False) as client:
    routed=[client.get(u).text for u in ['https://example.test:8443','https://unrelated.test','https://excluded.test']]
check('H07','specific mounts and exclusions override broad routes',routed==['port','broad','ordinary'],{'routes':routed})

async def asgi_probe():
    scopes=[]
    async def app(scope,receive,send):
        scopes.append(scope['type'])
        await send({'type':'http.response.start','status':200,'headers':[]})
        await send({'type':'http.response.body','body':b'ok'})
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),trust_env=False) as client:
        await client.get('https://example.test')
    check('H10','ASGI transport issues HTTP scope without lifespan scopes',scopes==['http'],{'scope_types':scopes})
asyncio.run(asgi_probe())

source=ROOT/'sources/paperless-ngx/src/paperless/parsers/registry.py'
tree=ast.parse(source.read_text())
original=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ParserRegistry')
method=next(n for n in original.body if isinstance(n,ast.FunctionDef) and n.name=='get_parser_for_file')
cls=ast.ClassDef(name='RegistryProbe',bases=[],keywords=[],body=[copy.deepcopy(method)],decorator_list=[])
module=ast.fix_missing_locations(ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0),cls],type_ignores=[]))
namespace={'logger':logging.getLogger('probe')}
exec(compile(module,'upstream_registry_method','exec'),namespace)
def parser(name,score,remote=False):
    return type(name,(),{'name':name,'uses_remote_service':remote,'supported_mime_types':classmethod(lambda cls:{'application/test':'.test'}),'score':classmethod(lambda cls,*args:score)})
builtin=parser('BuiltIn',10);external=parser('External',10);declined=parser('Declined',None);remote=parser('Remote',20,True)
reg=namespace['RegistryProbe']();reg._builtins=[builtin];reg._external=[external]
result=reg.get_parser_for_file('application/test','sample.test')
check('P16','external parser wins equal score',result is external,{'winner':result.name})
reg._external=[declined]
result=reg.get_parser_for_file('application/test','sample.test')
check('P16','None score declines selection',result is builtin,{'winner':result.name})
reg._external=[remote]
result=reg.get_parser_for_file('application/test','sample.test',allow_remote=False)
check('P17','declared remote parser excluded when not allowed',result is builtin,{'winner':result.name})
result=reg.get_parser_for_file('application/test','sample.test',allow_remote=True)
check('P17','declared remote parser eligible when allowed',result is remote,{'winner':result.name})

consumer=ROOT/'sources/paperless-ngx/src/documents/consumer.py'
tree=ast.parse(consumer.read_text())
method=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='should_produce_archive')
module=ast.fix_missing_locations(ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0),copy.deepcopy(method)],type_ignores=[]))
namespace={'logging':logging,'LOGGING_NAME':'probe','OcrConfig':lambda:types.SimpleNamespace(archive_file_generation='never'),'ArchiveFileGenerationChoices':types.SimpleNamespace(ALWAYS='always',NEVER='never')}
exec(compile(module,'upstream_archive_function','exec'),namespace)
required=types.SimpleNamespace(requires_pdf_rendition=True,can_produce_archive=True)
optional=types.SimpleNamespace(requires_pdf_rendition=False,can_produce_archive=True)
result=namespace['should_produce_archive'](required,'application/test',Path('unused'))
check('P13','mandatory rendition overrides never archive mode',result is True,{'produce_archive':result})
result=namespace['should_produce_archive'](optional,'application/test',Path('unused'))
check('P13','never mode suppresses optional archive',result is False,{'produce_archive':result})

payload={'status':'Development definition probes, not blinded model trials, full-application tests or container isolation verification','network':'HTTPX uses local mock transports or an in-process ASGI application; these probes make no outbound HTTP requests','httpx_source':str(Path(httpx.__file__).resolve()),'dependency_versions':{name:importlib.metadata.version(name) for name in ['httpcore','anyio','certifi']},'paperless_isolation':'Actual upstream AST definitions executed with small stubs; application dependencies, storage and workers not exercised','checks':checks}
(ROOT/'local-runs/cross-repository-development-probes.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(checks),'checks':checks},indent=2))
