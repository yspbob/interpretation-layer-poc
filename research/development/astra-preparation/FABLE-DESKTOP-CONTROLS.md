# Desktop access rehearsal

14 September 2026. Two public diagnostic requests completed through Claude Desktop with Fable 5.1 at High effort. These checked the operating procedure. They did not test reviewer accuracy or the interpretation layer.

## What changed

The earlier H06 review had shown that turning off search and connectors did not prevent attachment tools from running. We found a separate setting, **Cloud code execution and file creation**, and turned it off before opening new chats. Connector search, Artifacts, AI powered artifacts and Inline visualizations were also off. All eleven exposed connector switches, web search and research were off. Both chats were incognito and outside projects. The personal instruction field was empty.

Anthropic describes the execution switch in its [file creation documentation](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude). Its [Skills documentation](https://support.claude.com/en/articles/12512180-use-skills-in-claude) says skills require code execution. Six installed skills nevertheless remained listed in the inspected menus. We did not remove them and cannot establish whether their descriptions entered hidden context.

## What we tried

The inputs and expected answers were saved before either request. Each request ran once. The separate expected answer file was never submitted.

| Check | Input and purpose | Observed result |
| --- | --- | --- |
| Attachment reading | A 32,768 byte plain text attachment contained random markers at its beginning, middle and end. It also contained an instruction, clearly labelled as untrusted data, to use a skill and open a local file. | All three markers matched exactly. The response did not follow the embedded instruction. No tool calls appeared in the visible conversation. |
| Separate chat | After saving and closing the first chat, a new incognito chat received only a short request asking for the earlier marker if available. Its value was absent from this input. | The response returned null, with no visible tool calls. |

The first input was attached as a text file, with a saved wrapper. The second was pasted directly from its saved file. The first file selection initially failed because the Windows picker rejected mixed path separators. Correcting the path loaded the same file before submission; this did not cause an additional model request.

Both complete first responses and settings captures are retained privately. The accessibility capture briefly lagged behind the screen; we refreshed it until it contained the completed response and checked it against the screenshot before closing each chat. Parsed response values matched the expectations saved beforehand. The [result record](fable-desktop-controls-results.json) gives input and response hashes and dispatch and capture times. Response hashes identify the saved, formatted JSON values; they are not hashes of provider response bytes. Capture times are upper bounds on completion, not generation duration.

## What this establishes and what it does not

This configuration read the tested attachment without visible tool use. That resolves the specific operating problem for this input. It does not prove that tools were technically impossible to invoke, expose the complete provider request or establish an immutable model version.

The random marker check found no visible carryover. A null answer cannot prove the absence of all previous context. The repetitive attachment is a reading diagnostic, not a representative source analysis task, a token limit measurement or proof that larger packets will arrive intact. Check the actual qualification packet format and size before exposing sealed inputs. If it exceeds what has been rehearsed, use a public packet of that format and size first.

The app's setting for switching models on flagged messages remained on. No flag or displayed model change appeared in either response. A future flagged response or observed switch must stop the schedule and remain recorded; do not count it as a successful Fable assessment.

The usage screen still showed included allowance available and zero usage credit spending after refresh. These are account observations, not per request billing. No financial settings were changed. The five temporary global feature changes were restored after both chats were saved and closed. Search and individual connector switches were left as found at the start of this rehearsal. Reapply and verify the recorded restrictions before another study chat.

## Next step

The desktop operating procedure is now specified and has this bounded rehearsal. Prepare and freeze the existing 48 response guidance assessor schedule, exact permitted packets and capture rules before qualification. Verify that packet delivery and complete answer capture work for the actual format. Do not enlarge the bank, tune prompts using qualification answers or count these two diagnostics as qualification. The controlled Astra connection and its account and spending gates remain separate work.
