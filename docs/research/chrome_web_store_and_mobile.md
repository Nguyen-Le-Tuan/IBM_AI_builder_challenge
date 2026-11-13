# Chrome Web Store publishing and mobile routes — research, 2026-11-12

`VERIFIED` means the primary page was opened in this run and a short quote (at most 25 words) is given. `NOT VERIFIED` means the page could not be opened or only a secondary source was seen. This is not legal advice. Note on method: pages were read through a fetch tool that returns a summary with quoted fragments; quoted fragments are as returned and should be re-read on the page before anything is submitted. 

## 1. Chrome Web Store account and process

| Topic | Primary source and short quote | What it means for us | Tag |
|---|---|---|---|
| Registration fee exists | [Register](https://developer.chrome.com/docs/webstore/register): "you must register as a CWS developer and pay a one-time registration fee" | One-time fee; the page states no amount. | `VERIFIED` |
| Fee amount ($5) | Not on the pages opened (register, set-up-account, FAQ). Only third-party blogs (search results) say $5. | Treat $5 as unconfirmed until the dashboard shows it. | `NOT VERIFIED` |
| Developer email | [Register](https://developer.chrome.com/docs/webstore/register): "After an account is created, you cannot change its email address." | Use a dedicated team address, not a personal one. | `VERIFIED` |
| Contact email verification | [Set up account](https://developer.chrome.com/docs/webstore/set-up-account): "Verifying your contact email address is required when you set up a new developer account." | Verification link is sent by the store. | `VERIFIED` |
| Publisher name | Same page: appears under "Offered by:" in the listing details; verified publishers can show a URL. | Decide a public publisher name. | `VERIFIED` |
| Supported regions | [Register](https://developer.chrome.com/docs/webstore/register): registration only in listed countries, including US, Canada, UK (summary of page). | Check the team's country on the page. | `VERIFIED` |
| 2-step verification | Not mentioned on register, set-up-account, or FAQ pages. Third-party blogs say it is required. | Assume it is needed; confirm in the dashboard. | `NOT VERIFIED` |
| Trader / non-trader declaration | Not mentioned on pages opened. `developer.chrome.com/docs/webstore/trader-verification` and a support.google.com page returned 404. Blogs say every developer must choose. | Open question; confirm in dashboard Account tab. | `NOT VERIFIED` |
| Visibility: public | [Distribution](https://developer.chrome.com/docs/webstore/cws-dashboard-distribution): "This option lists your item on the Chrome Web Store for all users to see and install." | Goal for the real launch. | `VERIFIED` |
| Visibility: unlisted | Same: anyone can install "if they know its Chrome Web Store URL." | Good for a demo/judge link. | `VERIFIED` |
| Visibility: private / trusted testers | Same: private "limits installation of your item to specified users only"; trusted testers are tied to Google Accounts, list belongs to the account. | Good for team testing before launch. | `VERIFIED` |
| Review time | [Review process](https://developer.chrome.com/docs/webstore/review-process): "For most extensions, review is completed within a few days, but it can take up to a few weeks." | Submit early; do not plan a hard date. | `VERIFIED` |
| Slower review signals | Same: new developers, new extensions, dangerous permissions, significant code changes; "broad host permissions or sensitive execution permissions" take longer. | We are a new developer; keep permissions small. | `VERIFIED` |
| Package size | [Publish](https://developer.chrome.com/docs/webstore/publish): "The maximum supported file size for an extension package is 2GB." | Tesseract.js plus language data fits. | `VERIFIED` |
| Publish steps | Same: sign in to the dashboard, "Add new item", upload the ZIP, fill the tabs, "Submit for Review". | Matches checklist. | `VERIFIED` |
| Icon | [Images](https://developer.chrome.com/docs/webstore/images): "You must provide a 128x128-pixel extension icon image in the ZIP file of your extension" (artwork 96x96). | Need 128x128 icon. | `VERIFIED` |
| Screenshots | Same: "at least 1—and preferably the maximum allowed 5—screenshots", 1280x800 or 640x400. | Prepare 3-5 at 1280x800. | `VERIFIED` |
| Promo images | Same: small 440x280 and marquee 1400x560, described as optional. | Optional. | `VERIFIED` |
| Description, category, language fields | The publish page does not name them ("details of your listing"). | Not found; see dashboard. | `NOT VERIFIED` |

## 2. Program policies that touch this product

Policy page: [Chrome Web Store program policies](https://developer.chrome.com/docs/webstore/program-policies/policies).

| Topic | Primary source and short quote | What it means for us | Tag |
|---|---|---|---|
| Single purpose | Policies: "An extension must have a single purpose that is narrow and easy to understand." | Purpose statement: check a selected post against its cited source and highlight differences. No extra features. | `VERIFIED` |
| Minimum permissions | Policies: "Request access to the narrowest permissions necessary to implement your Product's features or services." | Prefer `activeTab`; see "Smallest permission set". | `VERIFIED` |
| Limited Use / necessary data | Policies: "Extensions may only collect, use, or transmit user data that is necessary for the extension's disclosed single purpose" | Selected text sent only to our backend for the check. | `VERIFIED` |
| Privacy policy required | Policies: "If your Product handles any user data, then you must post an accurate and up to date privacy policy." [User data FAQ](https://developer.chrome.com/docs/webstore/program-policies/user-data-faq): "Website content and resources" and "Personal communications" are listed as user data. | We transmit selected page text, so we need a privacy policy. | `VERIFIED` |
| Limited Use disclosure | User data FAQ: "All extensions that request user data must show a Limited Use disclosure on your project's homepage." | Add the disclosure to a project homepage. | `VERIFIED` |
| HTTPS | User data FAQ: "Extensions must transmit user data over a secure connection (e.g. HTTPS, WSS)." | Backend must be HTTPS. | `VERIFIED` |
| Dashboard privacy tab | [Privacy tab](https://developer.chrome.com/docs/webstore/cws-dashboard-privacy): "You must disclose how your extension collects and uses user data." Also single-purpose field, per-permission justification, remote code field. | Fill all fields; disclosures must match the privacy policy. | `VERIFIED` |
| Remote code (MV3) | Policies: "Execution of logic from a remote source is permissible only when accomplished through a documented API". [MV3 requirements](https://developer.chrome.com/docs/webstore/program-policies/mv3-requirements): external resources may supply data but "must not contain logic" (paraphrase). | Do not load scripts or WASM from a CDN; bundle everything. | `VERIFIED` |
| Calling own backend API | [Improve security](https://developer.chrome.com/docs/extensions/develop/migrate/improve-security): "You can still load data remotely at runtime." Suggests "Your extension calls a remote web service." Service must not return code to execute. | Our FastAPI backend returning JSON findings is allowed. | `VERIFIED` |
| eval | Same page: "You can no longer execute external logic using executeScript(), eval(), and new Function()." | Do not eval LLM output. | `VERIFIED` |
| Obfuscation | Policies: "Developers must not obfuscate code or conceal functionality of their extension." Review page: minified code can be harder to review. | Ship readable or plain-minified code, with source available. | `VERIFIED` |
| Misleading claims | Policies: "We do not allow products that deceive or mislead users, including in the content, title, description, or screenshots." | Do not claim "fact-checking truth"; say it compares a post with its cited source. | `VERIFIED` |
| Health/medical | Policies mention only regulated goods including "health/medical devices"; no dedicated health-content section found in the text returned. | No explicit rule found; avoid medical-advice claims. | `VERIFIED` (absence in text read) |
| AI-generated content | Not addressed in the text returned. | No rule found on this page; re-check the full policy page manually. | `NOT VERIFIED` |
| Altering third-party pages | Only provision found concerns ads: "Ads associated with your product may not interfere with any ads on a third-party website". No general rule found. | Highlighting user-selected text is not covered by an explicit rule found here. | `VERIFIED` (absence in text read) |

## 3. Manifest V3 specifics

| Topic | Primary source and short quote | What it means for us | Tag |
|---|---|---|---|
| MV2 status | [MV2 timeline](https://developer.chrome.com/docs/extensions/develop/migrate/mv2-deprecation-timeline): "all users on all channels of Chrome have now Manifest V2 extensions disabled." Remaining MV2 extensions removed from the store 31 Aug 2026. | MV3 only. | `VERIFIED` |
| activeTab | [activeTab](https://developer.chrome.com/docs/extensions/develop/concepts/activeTab): "gives an extension temporary access to the currently active tab"; triggered by executing an action, a context menu item, shortcuts. Revoked on navigating away or closing the tab. | Fits click-to-check and context menu. | `VERIFIED` |
| activeTab warning | Same page: "displays no warning message during installation." [Permission warnings](https://developer.chrome.com/docs/extensions/develop/concepts/permission-warnings): "This permission does not display a permission warning." | No install warning. | `VERIFIED` |
| activeTab and executeScript | activeTab page: can "Call scripting.executeScript() on that tab" if "scripting" is declared. | Need `scripting` to inject the highlighter. | `VERIFIED` |
| activeTab and captureVisibleTab | The activeTab page did not mention it. | Open question for OCR route. | `NOT VERIFIED` |
| scripting | [scripting](https://developer.chrome.com/docs/extensions/reference/api/scripting): "declare the "scripting" permission in the manifest plus the host permissions" — or `activeTab`. | Use `activeTab` as the host grant. | `VERIFIED` |
| contextMenus | [contextMenus](https://developer.chrome.com/docs/extensions/reference/api/contextMenus): "You must declare the "contextMenus" permission"; `OnClickData.selectionText`: "The text for the context selection, if any." Install warning not stated on the page. | Context menu on "selection" gives selected text. | `VERIFIED` |
| storage | [storage](https://developer.chrome.com/docs/extensions/reference/api/storage): "declare the "storage" permission"; local limit 10 MB. | Only if we store settings. | `VERIFIED` |
| offscreen | [offscreen](https://developer.chrome.com/docs/extensions/reference/api/offscreen): "declare the "offscreen" permission"; reason WORKERS; "The runtime API is the only extensions API supported by offscreen documents." One open at a time. | Only needed if OCR runs in an offscreen document. | `VERIFIED` |
| host_permissions vs optional | [Declare permissions](https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions): `optional_host_permissions` are "Granted by the user at runtime, instead of at install time." | Backend host can be a required host permission, or use CORS. | `VERIFIED` |
| Runtime request | [permissions API](https://developer.chrome.com/docs/extensions/reference/permissions): "Permissions must be requested from inside a user gesture, like a button's click handler." | Fine for optional OCR feature. | `VERIFIED` |
| Content-script network | [Network requests](https://developer.chrome.com/docs/extensions/develop/concepts/network-requests): content scripts are subject to cross-origin rules; "do not allow content scripts to request an arbitrary URL." | Send the request from the service worker, to a fixed backend URL. | `VERIFIED` |
| CSP and WASM | [CSP](https://developer.chrome.com/docs/extensions/mv3/manifest/content_security_policy): default `extension_pages` "script-src 'self'; object-src 'self';" (WebAssembly disabled); minimum policy allowing WASM "script-src 'self' 'wasm-unsafe-eval'; object-src 'self';". Improve-security page: directives may use only `'self'`, `'none'`, `'wasm-unsafe-eval'`. | Tesseract.js WASM in an extension page needs `'wasm-unsafe-eval'`, bundled locally. Whether it works in content scripts: not stated. | `VERIFIED` |
| Service worker lifetime | [Lifecycle](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle): "After 30 seconds of inactivity"; single event over 5 minutes, or a fetch response over 30 seconds, ends it. | LLM call should return within 30 s or use streaming/polling. | `VERIFIED` |


## 4. Mobile routes

| Topic | Primary source and short quote | What it means for us | Tag |
|---|---|---|---|
| Chrome for Android extensions | No primary page opened states a position. [Extensions overview](https://developer.chrome.com/docs/extensions/develop), the getting-started page and the [manifest reference](https://developer.chrome.com/docs/extensions/reference/manifest) do not mention Android. A guessed page (`differences-with-chrome-on-android`) returned 404. | Do not assume Chrome for Android runs extensions. Not found, not a "no". | `NOT VERIFIED` |
| Firefox for Android: support | [Extension Workshop](https://extensionworkshop.com/documentation/develop/differences-between-desktop-and-android-extensions/): "Firefox for Android offers a subset of the WebExtensions APIs available to the desktop version of Firefox." | A subset of APIs; `menus`, `commands`, `windows` and others are unsupported. | `VERIFIED` |
| Firefox for Android: permissions and background | Same page: "on Firefox for Android permissions are granted automatically and the user isn't given the option to deny them." Background scripts should be non-persistent. | Avoid APIs on the unsupported list; the context menu route may not work on Android. | `VERIFIED` |
| Firefox for Android: testing | [Developing for Firefox for Android](https://extensionworkshop.com/documentation/develop/developing-extensions-for-firefox-for-android/): run `web-ext run -t firefox-android`; manifest `gecko_android` sets a separate compatibility range. | Testable with a USB device and `web-ext`. | `VERIFIED` |
| Publishing on AMO | [Submitting an add-on](https://extensionworkshop.com/documentation/publish/submitting-an-add-on/): "Submit a New Add-on"; choose listed "On this site" or "On your own"; "The maximum file size accepted is 200 MB." No fee mentioned. Source package needed for minified or obfuscated code. | Free Mozilla account; keep readable source. 200 MB limit matters for OCR language data. How Android users find it on AMO: not found. | `VERIFIED` |
| Edge for Android | [Edge mobile FAQ](https://support.microsoft.com/microsoft-edge/microsoft-edge-for-mobile-faqs-29296eab-b76f-4a87-ac9c-9835da53465d) (Microsoft support site, not on the preferred list): "continues to support Adblock Plus and Coupons." Names only those two built-in extensions. | No evidence that third-party extensions can be installed. | `VERIFIED` (limited) |
| Safari on iOS/iPadOS: packaging | [Apple docs JSON feed for "Packaging a web extension for Safari"](https://developer.apple.com/tutorials/data/documentation/safariservices/packaging-a-web-extension-for-safari.json): tool is `safari-web-extension-packager`, which "used to be named `safari-web-extension-converter`"; run `xcrun safari-web-extension-packager /path/to/extension`. The normal HTML page returned only its title. | Chrome extension can be wrapped into an iOS app project; the converter tool was renamed. | `VERIFIED` (via JSON feed) |
| Safari: Mac, Xcode, developer programme | Same source: usable "alongside Xcode on a Mac"; a web-based alternative in App Store Connect lets you distribute "without a Mac or Xcode" (paraphrase). The Apple Developer Program, its fee, and iPadOS were not mentioned. | A Mac is the default path; fee and programme rules: not found. | `NOT VERIFIED` (programme, fee, iPadOS) |
| Web Share Target: manifest | [MDN share_target](https://developer.mozilla.org/en-US/docs/Web/Manifest/share_target): "To accept shared files, the HTTP method must be `POST`, the `enctype` must be `multipart/form-data`, and a `files` entry..." Params `title`, `text`, `url` name the fields. | A PWA could receive text, URL and images from the system share sheet. | `VERIFIED` |
| Web Share Target: install requirement | MDN: "Your PWA can only act as a web share target if it has been installed." [web.dev/Chrome docs](https://developer.chrome.com/docs/capabilities/web-apis/web-share-target): "On all platforms, your web app has to be installed before it will show up as a potential target for receiving shared data." | User must install the PWA first. | `VERIFIED` |
| Web Share Target: support | Chrome docs: "Chrome 76 or later for Android, or Chrome 89 or later on desktop". MDN: "This feature is not Baseline because it does not work in some of the most widely-used browsers." The page does not mention iOS; MDN's compat table did not load. | Android Chrome works; iOS support: not found. | `VERIFIED` (Chrome), `NOT VERIFIED` (iOS, Firefox, Safari) |
| Web Share Target: spec status | [W3C draft](https://w3c.github.io/web-share-target/): "This is an early draft of the Web Share Target spec." The spec does not require installation: user agents are "NOT REQUIRED to 'register' web share targets at all." The TR URL returned 404. | Not a stable standard. | `VERIFIED` |
| Web Share (sending side) | [MDN navigator.share](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share): "not Baseline"; HTTPS only. Whether native social apps offer a share sheet is outside these pages. | Depends on the social app offering Share; not documented here. | `VERIFIED` |

## 5. Cross-browser

| Topic | Primary source and short quote | What it means for us | Tag |
|---|---|---|---|
| Namespaces | [MDN build a cross-browser extension](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Build_a_cross_browser_extension): "Firefox also supports the `chrome.*` namespace for APIs that are compatible with Chrome". [MDN differences](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Differences_between_API_implementations): `browser` used "from Chrome 148, in Chrome, Edge, and Opera". | Pages show dates later than our knowledge; check against the live pages. | `VERIFIED` |
| Promises | MDN differences: "full coverage in Chrome 152." | Promise style works in recent Chrome. | `VERIFIED` |
| webextension-polyfill | MDN: "In Chrome 152 or later, the polyfill is no-op." [Mozilla repo](https://github.com/mozilla/webextension-polyfill) (not on the preferred list): "will not receive any further updates"; repository archived. | Optional for older browsers; do not depend on it. | `VERIFIED` |
| Firefox background | [MDN background](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/background): "`background.service_worker` is not supported (see Firefox bug 1573659)." Cross-browser pattern: list both `scripts` and `service_worker`. | One manifest can serve both, with an event page in Firefox. | `VERIFIED` |
| Edge Add-ons: account and process | [Edge publish](https://learn.microsoft.com/en-us/microsoft-edge/extensions/publish/publish-extension): developer account via Partner Center; "The certification process can take up to seven business days". No fee mentioned. | Chrome package can be submitted; Edge visibility is Public or Hidden. | `VERIFIED` |
| Edge listing | Same page: description minimum 250 characters; logo recommended 300x300; screenshots 640x480 or 1280x800, maximum 6. Privacy page has single purpose, permission justification, remote code, data usage, privacy policy URL. "Remote code is only supported for Manifest V2." | Same disclosures as Chrome. | `VERIFIED` |

## Publishing checklist

1. Decide a team publisher address and register the developer account; the email cannot be changed (section 1: Developer email, Registration fee). Confirm fee, 2-step verification and trader status in the dashboard (rows marked `NOT VERIFIED`).
2. Write the single-purpose statement: "check a user-selected post against its cited source" (section 2: Single purpose).
3. Build MV3 only; bundle all code, including any WASM and OCR data, locally; no remote scripts (section 2: Remote code; section 3: CSP and WASM).
4. Send selected text to the backend as JSON from the service worker only, over HTTPS, to a fixed URL; never eval returned content (section 2: Calling own backend API, HTTPS; section 3: Content-script network).
5. Keep permissions minimal (see "Smallest permission set"); write a justification for each (section 2: Dashboard privacy tab; section 1: Slower review signals).
6. Write and host a privacy policy and a Limited Use disclosure on a project homepage; state that post text is not stored, only hashes, evidence URLs and outputs (section 2: Privacy policy required, Limited Use disclosure). The team must make sure this matches the backend.
7. Keep code readable; no obfuscation (section 2: Obfuscation).
8. Prepare listing assets: 128x128 icon, 3-5 screenshots at 1280x800, optional promo tiles (section 1: Icon, Screenshots, Promo images).
9. Keep listing claims honest: compares to the cited source; no truth or medical claims (section 2: Misleading claims, Health/medical).
10. Test with Private or trusted testers first, then Unlisted, then Public (section 1: Visibility).
11. Submit; allow days to weeks (section 1: Review time).
12. Optional later: Edge Add-ons from the same package; Firefox build with `scripts` background (section 5).

## Smallest permission set

`RECOMMENDED (not decided)`. These are suggestions from the documentation read; they are untested.

| Version | Permissions | Reason |
|---|---|---|
| (a) Text-only MVP | `activeTab`, `scripting`, `contextMenus`; `host_permissions` for the backend URL only (or rely on backend CORS) | `activeTab`: temporary access, no install warning. `scripting`: inject highlighter on user click. `contextMenus`: the "Check" menu on selection (`selectionText`). Backend host so the service worker can fetch. No `storage`, no `<all_urls>`. Whether `scripting` and `contextMenus` show install warnings: not stated on pages read. |
| (b) Image/OCR | Same as (a), plus either `offscreen` (OCR in an offscreen document with reason WORKERS) or an extension page, and `content_security_policy.extension_pages` with `'wasm-unsafe-eval'`; for screenshot route `tabs.captureVisibleTab` | Tesseract.js WASM needs `'wasm-unsafe-eval'` and local files. `offscreen` allows only the runtime API. Whether `activeTab` covers `captureVisibleTab`: not found in the page read; test it. Optional: `optional_host_permissions` for any extra hosts, requested on a click. |

## Mobile options compared

| Option | Reach | Effort | Blockers |
|---|---|---|---|
| Chrome for Android extension | Largest mobile browser, if supported | Unknown | No primary statement found; not verified |
| Firefox for Android | Small share, but real extensions | Low to medium: Firefox build, AMO listing | Subset of APIs; context menu API unsupported; only in-browser, not native apps |
| Edge for Android | Small | n/a | No evidence of third-party extension support |
| Safari iOS extension | iPhone/iPad Safari users | High: Mac, Xcode, app wrapper | Developer programme and fee not verified; only inside Safari |
| Web Share Target PWA | Android Chrome users in native apps via share sheet | Medium: PWA plus backend page | Installed PWA needed; spec is a draft; iOS support not found; depends on each app offering Share |

Note: none of these routes reads social platforms; a user shares text or images they choose.

## Open questions

- Registration fee amount, 2-step verification and trader status: confirm in the Developer Dashboard (primary pages opened did not state them).
- Does Chrome for Android support extensions today? No primary page found.
- Does `activeTab` permit `tabs.captureVisibleTab`? Not stated on the activeTab page.
- Do `scripting` and `contextMenus` produce install warnings? The pages read did not say; check the permissions list page.
- Does Chrome Web Store policy say anything on AI-generated content? Not found in the text read; read the full policy page manually.
- Does WASM run in content scripts or only extension pages? Not stated.
- Apple Developer Program fee and rules; iPadOS support: not found.
- Does Web Share Target work on iOS Safari? Not found.
- Do the backend and privacy policy match the policy statement "stores hashes, not post text"? Needs team decision (legal review not done).

Prompt-injection note: no instruction-like text addressed to the agent was seen in any page.
