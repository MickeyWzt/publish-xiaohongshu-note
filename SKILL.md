---
name: publish-xiaohongshu-note
description: Publish prepared Xiaohongshu image notes through the user's logged-in Chrome session, including duplicate checks, ordered multi-image upload, title and body entry, truthful original or AI-content declarations, final publish authorization, recovery from stale tabs or file-chooser failures, and verification in Note Manager. Use when the user asks Codex to upload, test-publish, directly publish, retry, or verify a Xiaohongshu image-and-text post; also use for scheduled Xiaohongshu publishing runs whose assets and copy are already prepared.
---

# Publish a Xiaohongshu image note

Use the creator website in the user's logged-in Chrome session. Optimize for one clean publish attempt, exact verification, and safe recovery.

## Required browser setup

1. Read the currently available `chrome:control-chrome` skill completely before browser work.
2. Use Chrome when the user requests Chrome or the workflow depends on its logged-in Xiaohongshu session. Do not substitute another browser.
3. Initialize the browser runtime once, read Chrome's complete documentation, and reuse the browser binding.
4. Name the session clearly, such as `📝 小红书发布`.
5. Never inspect or extract cookies, local storage, passwords, QR codes, or verification codes.

## Decide the authorized stopping point

Classify the request before opening the creator page:

- **Prepare only:** do not open the publish page or upload.
- **Draft/upload only:** fill the post, verify the draft, and stop before the final publish action.
- **Publish:** click the final publish control only when the current user request or active automation explicitly authorizes direct publishing.

Treat “content is ready” and “upload it” as insufficient authority for the final publish action. If login, CAPTCHA, QR scanning, or account verification is required, pause for the user without requesting or handling credentials.

## Preflight the package

Before browser mutation:

1. Resolve every image to an absolute local path in final display order.
2. Confirm that all files exist, are readable images, and match the intended cover-to-summary sequence.
3. Read the exact title, body, source text, tags, and any publishing notes from the package.
4. Check title/body limits against the current page instead of trusting remembered limits.
5. Decide whether `原创声明`, AI-generated-content labeling, commercial disclosure, or topic/activity selection applies. Set these truthfully; never use a label merely to improve reach.
6. For scheduled runs, retries, or possible partial failures, inspect `笔记管理` first and search for the same title/topic to prevent a duplicate.

## Fast publish path

1. Open a fresh tab at `https://creator.xiaohongshu.com/publish/publish?from=menu&target=image`.
2. Wait for the image-post form and the visible, enabled `上传图片` button. Allow extra navigation time for the creator site.
3. Start the `filechooser` wait **before** clicking the visible `上传图片` button.
4. Click that visible button, receive the chooser, then set the complete ordered file list in one call.
5. Wait for processing. Verify the thumbnail count and order before entering text.
6. Fill title and body with semantic locators. Verify the actual field values and live character counters after filling.
7. Apply required declarations through their visible UI. Verify the resulting page state, such as `已声明原创`.
8. Run the terminal pre-publish check below.
9. If authorized, click the exact final `发布` control while waiting for the resulting navigation or page-state change.
10. Verify the success page, then open `https://creator.xiaohongshu.com/new/note-manager` and locate the exact title plus its status.

Do not operate a hidden `input[type=file]` as the primary upload route. In repeated successful runs, the reliable sequence was: wait for chooser → click visible upload button → set all files.

## Terminal pre-publish check

Do not click `发布` until all checks pass:

- Expected image count and cover/order are visible.
- Title exactly matches the approved title.
- Body, sources, and tags are complete and within the live limit.
- Required original/AI/commercial labels show the intended final state.
- No unresolved crop, upload, quality, moderation, or validation warning remains.
- The exact final publish control is present and enabled.
- The request still authorizes publishing now.

Take a current screenshot when the final button or a declaration control cannot be addressed semantically. Derive coordinates from that screenshot; never reuse coordinates from an earlier run.

## Recovery rules

- On a stale/missing tab, discard only the tab binding. Reuse the browser binding and claim or create a fresh tab.
- On slow navigation, reacquire the current page or open one clean publishing tab; do not repeatedly initialize browser runtimes.
- On file-chooser timeout, inspect whether any thumbnails were added. If none were added, open a clean publish tab and retry through the visible button. If some were added, inspect the draft before any retry to avoid duplicates.
- If direct checkbox actions fail for `原创声明`, click the visible declaration row/switch, complete the modal agreement, click the semantic `声明原创` button, and verify `已声明原创`.
- If the final publish button is off-screen, adjust the viewport or scroll, capture a fresh screenshot, click once, and then restore the viewport.
- On CAPTCHA, account risk control, login expiry, or ambiguous publish outcome, stop. Preserve the useful tab and report the exact state.

Read [references/publishing-playbook.md](references/publishing-playbook.md) for concrete browser-action patterns, failure diagnosis, and result-verification criteria.

## Report only verified outcomes

Distinguish these states precisely:

- `草稿已填好`: fields and media are present; publish was not clicked.
- `已提交/审核中`: the platform accepted the publish action and Note Manager shows the note under review.
- `已发布`: the public/live state is confirmed, when the platform exposes that state.
- `状态不明`: the click occurred but neither a success page nor Note Manager provides confirming evidence.

Include the exact title, image count, declaration state, platform status, and visible publish time when available. Keep the result tab as the deliverable; close only task-created disposable tabs and preserve the user's unrelated tabs.
