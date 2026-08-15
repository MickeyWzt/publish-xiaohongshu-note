# Xiaohongshu publishing playbook

Use this reference after reading the parent `SKILL.md`. Page labels and layout can change; prefer current semantic text and current screenshots over remembered selectors or coordinates.

## Stable browser-action pattern

The following pseudocode expresses the reliable order. Adapt variable names and the current browser API documentation.

```js
// Reuse an initialized Chrome binding and a fresh task tab.
const tab = await chrome.tabs.new();
await tab.goto("https://creator.xiaohongshu.com/publish/publish?from=menu&target=image");

const uploadButton = tab.playwright.getByRole("button", {
  name: "上传图片",
  exact: true,
});

await uploadButton.waitFor({ state: "visible" });
const chooserPromise = tab.playwright.waitForEvent("filechooser", {
  timeoutMs: 12000,
});
await uploadButton.click();
const chooser = await chooserPromise;
await chooser.setFiles(absoluteOrderedImagePaths, { timeoutMs: 30000 });
```

Why this order matters:

- Clicking a hidden file input directly repeatedly timed out or reset the controlled tab.
- Starting the chooser wait after the click can miss the event.
- Uploading the complete ordered list at once preserves sequence and avoids repeated chooser races.

After `setFiles`, wait for upload/processing to settle and inspect the live DOM or screenshot. A visible counter such as `5/18` was useful in prior runs, but verify the current UI rather than hard-coding it.

## Filling the post

Prefer semantic locators anchored by current page labels:

```js
const title = tab.playwright.getByPlaceholder("填写标题会有更多赞哦");
await title.fill(postTitle);

// Identify the body field from the current DOM. Do not blindly assume nth(1)
// if more textboxes are present.
const body = /* current visible body editor */;
await body.fill(postBody);
```

Immediately reread:

- title field value;
- body text or editor content;
- live character counters;
- selected topics/tags;
- media count and order.

Avoid filling before image processing finishes if the page is still replacing or re-rendering the form.

## Original declaration flow

The declaration uses a switch plus a confirmation modal. The underlying checkbox may be invisible or reject direct `check()`/`click()` calls.

1. Locate visible text `原创声明`.
2. Try a semantic click on its visible row or switch.
3. If that fails, capture a fresh screenshot and click the currently visible switch using coordinates derived from that screenshot.
4. In the modal, select `已阅读并同意《原创声明须知》`.
5. Confirm that the `声明原创` button becomes enabled.
6. Click the exact `声明原创` button.
7. Verify that the main form shows `已声明原创`.

Do not reuse old coordinates. Prior viewport sizes and page scroll positions are not stable.

## Final publish and verification

Prefer a semantic exact-match publish button. If the visible button cannot be reached semantically, capture a fresh screenshot and click its current location once.

```js
const publish = tab.playwright.getByRole("button", {
  name: "发布",
  exact: true,
});

// Use the current browser documentation's navigation/page-state waiting API.
await tab.playwright.expectNavigation(
  () => publish.click(),
  { timeoutMs: 30000, waitUntil: "domcontentloaded" },
).catch(() => null);
```

A navigation timeout does not prove failure. Inspect the resulting URL and DOM, then open Note Manager and search for the exact title.

Acceptable evidence hierarchy:

1. Success page or explicit successful-result state after the click.
2. Exact title in Note Manager with `审核中`, `已发布`, or another explicit platform status.
3. Visible publish time/status associated with that exact title.

A toast alone, an enabled button disappearing, or a click completing is insufficient evidence.

## Failure and recovery matrix

| Symptom | Likely cause | Recovery |
|---|---|---|
| Creator navigation times out | Slow site load or stale controlled tab | Reuse Chrome binding; reacquire the tab or create one clean publish tab; allow a longer navigation timeout. |
| Direct file input click fails | Hidden/unstable upload control | Listen for `filechooser` first, then click visible `上传图片`. |
| File chooser opens but files do not appear | Tab reset, stale chooser, or processing delay | Reconnect to current Chrome, inspect thumbnails, and retry only if the draft is still empty. |
| Reclaimed tab hangs | Stale tab binding | Discard only that tab binding and create a fresh task tab. |
| Original checkbox rejects direct click | Custom switch and modal workflow | Click visible declaration UI, accept the modal, then verify `已声明原创`. |
| Publish button is below the fold | Viewport/scroll mismatch | Resize or scroll, take a fresh screenshot, click once, then restore viewport. |
| Click returns no clear success | Navigation timing or platform delay | Inspect current URL/DOM and verify exact title in Note Manager. Report `状态不明` if neither confirms. |
| Login/QR/CAPTCHA/risk control appears | Authentication or platform intervention | Stop and hand the visible page to the user. Never handle secrets or bypass controls. |

## Speed without sacrificing correctness

- Use one clean publishing tab and one Note Manager verification step.
- Upload all images in one chooser call.
- Fill title and body only after upload processing stabilizes.
- Batch terminal checks into one DOM read where practical.
- Do not keep retrying the same stale tab.
- Do not repeat expensive browser initialization after a tab-only failure.
- Preserve the result tab so the user can inspect it immediately.
