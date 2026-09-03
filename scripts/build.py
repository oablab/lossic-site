#!/usr/bin/env python3
"""Build lossic.app — four standalone language pages from one template.

Follows foldic.app's architecture: per-language directories (/, /zh/, /ja/, /ko/),
full standalone HTML per language with hreflang alternates, first-visit locale
routing on the root page, and an explicit choice stored in localStorage.

Fonts are per-language, and that is the point of generating rather than copying:
CJK text set in a Latin serif falls back per-glyph and looks broken. Each language
carries its own body and heading stacks (PingFang TC / Songti TC for zh-Hant,
Hiragino for ja, Apple SD Gothic Neo for ko) plus CJK-appropriate line-height and
zero letter-spacing.
"""
import os
import re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

L = {}

L["en"] = {
    "lang_attr": "en", "path": "/", "dir": "",
    "font_body": '-apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif',
    "font_head": '"New York", Georgia, "Times New Roman", serif',
    "line_height": "1.65", "letter_spacing": "-0.02em",
    "title": "Lossic — The lossless player that tells the story behind your music",
    "desc": "Lossic streams ALAC and FLAC straight from your own Google Drive — no servers in between, no re-encoding, playback in about a fifth of a second. Swipe right, and it introduces the performer and the piece you're hearing.",
    "og_title": "Lossic",
    "og_desc": "Your music collection, in your pocket — lossless from your own Google Drive, playing instantly, with every album's story one swipe away.",
    "nav": ["Features", "How it works", "FAQ"],
    "support": "Support",
    "h1": "Your music collection doesn't live on a shelf.<br><em>It lives in your pocket.</em>",
    "sub": "Lossless music in your own Google Drive, playing the moment you tap — no servers in between, no re-encoding. And with Lossic Pro on your Mac: insert a CD, and minutes later it plays on your iPhone. One unbroken pipeline, from disc to pocket.",
    "badge": "In development · coming to the App Store",
    "features_title": "Built like it's your library. Because it is.",
    "features": [
        ("bolt", "Instant play",
         "Tap and it's playing — about 0.2 seconds for a queued album track. Measured on real phones and real networks, not taken from marketing copy."),
        ("wave", "Original files, untouched",
         "ALAC and FLAC stream without re-encoding, from CD quality to high-resolution releases. A format badge tells you exactly what you're hearing."),
        ("lock", "Private by architecture",
         "Your iPhone talks to Google directly, read-only. Lossic runs no servers — we couldn't look at your library if we wanted to."),
        ("cloud", "Offline that just happens",
         "Every track you play stays cached on the phone. Play it again in a tunnel or on a plane — zero network required."),
        ("grid", "Albums that look like albums",
         "Covers, composers, disc numbers — read from your files' own tags. Classical albums finally make sense: browse by the composer, not just the performer."),
        ("box", "For real collections",
         "CD rips, Bandcamp and Qobuz purchases, live recordings. The library you actually own — not the one a store rents you."),
        ("book", "A player that tells the story",
         "Swipe right from Now Playing and Lossic introduces the performer and the piece — written by an AI from your file's own tags (and, with Gemini, the album cover). Tap a suggested question, or open Ask More and keep the conversation going."),
        ("key", "Your key, your AI",
         "Bring your own Gemini, OpenCode Zen or OpenRouter API key; it lives in the iOS Keychain and the app talks to the provider directly. Answers can come in English, Traditional or Simplified Chinese, Japanese, or Korean — your choice."),
    ],
    "how_title": "Two ways in, no setup",
    "how_sub": "No NAS, no port forwarding, no server to babysit.",
    "steps": [
        ("Your CD collection", "Insert a disc into a CD drive on your Mac. Lossic rips it to ALAC or FLAC, finds the album art and tags, writes everything in, and uploads it to the Lossic folder in your own Google Drive — automatically. Minutes later it's playing losslessly on your iPhone, with AI ready to tell its story."),
        ("Your existing FLAC/ALAC", "Already have lossless files? Import them right from your iPhone — pick an album's files from Google Drive or any Files location, and they land in your own Lossic space, playable immediately."),
        ("Then just listen", "Albums appear on your cover wall automatically. Played tracks stay on the phone — the music keeps going when the network doesn't."),
    ],
    "privacy_title": "No account. No server. No copy of your library.",
    "privacy_body": "Most cloud players route your files through their own machines. Lossic's entire backend is: none. Your files travel one hop, between Google and your devices, over a connection you can revoke any time — and Lossic can only ever see the files it created itself.",
    "faq_title": "FAQ",
    "faq": [
        ("Can Lossic see my music? Where does it go?",
         "Your device talks to Google Drive directly — there is no Lossic server, so nothing ever passes through us. Music you rip or import is uploaded straight from your device to your own Drive."),
        ("Can Lossic access everything in my Google Drive?",
         "No — and it couldn't even if it wanted to. Lossic uses Google's most limited permission, <em>drive.file</em>: it can only see files that Lossic itself created or imported. Everything outside that is invisible to the app — Google enforces this at the API level, it is not a promise we make. One practical consequence: FLAC/ALAC files you already keep in Drive must be brought in through the Import feature. Copying them into the Lossic folder in Drive's web UI won't work — visibility follows who created the file, not which folder it sits in."),
        ("Do you support iCloud?",
         "As an import source — yes, today: the import picker shows iCloud Drive alongside Google Drive, and anything you pick is uploaded into your Lossic space. As a storage backend — not yet, and there is an honest technical reason: iCloud offers third-party apps no partial-read streaming interface, so playing a cloud-only file would mean downloading it whole before it makes a sound. Google Drive's HTTP interface is what makes Lossic's instant start (~0.2s), smart caching and cellular data budgets possible. An iCloud backend may come later as a convenience option, clearly labelled as sync-then-play."),
        ("Do you support DSD?",
         "Not for playback — and that's Apple, not us: iOS has no DSD decoder, and the iPhone's hardware can't play the 1-bit stream natively. Apps that claim DSD support convert it to PCM on the fly, which sits badly with a product built on bit-honesty. If you have a DSD collection, convert it once to 24-bit ALAC or FLAC with a desktop tool and import that — a well-done DSD64 → 24/176.4 conversion is transparent, and we'd rather you do it once, knowingly, than have us do it silently on every play. Hi-res PCM (24/96, 24/192) plays natively and shows its true badge."),
        ("Which formats does it play?",
         "ALAC and FLAC as first-class citizens, plus AAC and MP3. High-resolution files play with their format shown on the face of the player."),
        ("Does streaming re-encode my files?",
         "Never. Lossic streams the original bytes of your file with HTTP range requests and does not transcode them on the way."),
        ("How fast is “instant”?",
         "A queued album track typically starts in about 0.2 seconds; a cold tap on a new file usually starts under a second on Wi-Fi. These are measured numbers from real devices, and staying honest about them is the whole product."),
        ("Why Google Drive?",
         "Because you already pay for the storage. Lossic adds the part that was missing: a player that treats your Drive like a local music library."),
        ("How does the story feature work?",
         "Swipe right from Now Playing and Lossic asks an AI to introduce the performer and the piece, using the track's embedded tags — and, with Gemini, the album cover — as context. Three suggested follow-up questions are one tap away, or open Ask More for a conversation about what's playing."),
        ("Do I need an AI subscription? What about my privacy?",
         "You bring your own API key — Gemini, OpenCode Zen or OpenRouter. It's stored in the iOS Keychain and the app calls the provider directly; there is still no Lossic server in the loop. With Gemini you can opt in to Google Search grounding for fresher answers. No key? The player works exactly the same — the story layer is simply off."),
        ("Can the AI get things wrong?",
         "Yes. The introductions are generated text and may contain mistakes — treat them as a knowledgeable friend's take, not a reference work. The playback numbers, by contrast, are measured."),
        ("When can I get it?",
         "Lossic is in active development and headed for the App Store. The page you're reading will grow a download button the day it ships."),
    ],
    "cta_title": "Own your music again.",
    "cta_button": "Coming to the App Store",
    "footer_note": "From the maker of <a href=\"https://foldic.app\">Foldic</a>.",
    "footer_rights": "© 2026 Lossic",
    "legal_privacy": "Privacy", "legal_terms": "Terms",
}

L["zh"] = {
    "lang_attr": "zh-Hant", "path": "/zh/", "dir": "zh",
    "font_body": '"PingFang TC", "SF Pro TC", -apple-system, BlinkMacSystemFont, "Heiti TC", "Microsoft JhengHei", sans-serif',
    "font_head": '"PingFang TC", "SF Pro TC", -apple-system, BlinkMacSystemFont, "Heiti TC", "Microsoft JhengHei", sans-serif',
    "head_weight": "800",
    "line_height": "1.85", "letter_spacing": "0.01em",
    "title": "Lossic — 會講故事的無損播放器",
    "desc": "Lossic 直接從你自己的 Google Drive 串流 ALAC 與 FLAC。中間沒有任何伺服器、不重新編碼——點下去零點二秒出聲。往右一滑，它還會介紹正在演奏的人與曲子。",
    "og_title": "Lossic",
    "og_desc": "你的音樂收藏，在你的口袋裡——你自己 Drive 上的無損音樂，一點即播；每張專輯的故事，一滑即得。",
    "nav": ["功能", "怎麼運作", "常見問題"],
    "support": "支援",
    "h1": '你的音樂收藏，不在書架上<br><em>在你的口袋裡</em>',
    "sub": "放在你自己 Google Drive 的無損音樂，一點即播——中間沒有伺服器、不重新編碼。配上 Mac 的 Lossic Pro：放入 CD，幾分鐘後 iPhone 直接播放。從光碟到口袋，一口氣解決。",
    "badge": "開發中 · 即將上架 App Store",
    "features_title": "把它當成你的音樂庫來打造——因為它本來就是。",
    "features": [
        ("bolt", "秒開播放",
         "點下去就出聲——佇列中的專輯曲目約 0.2 秒。這是真手機、真網路量出來的數字，不是文案。"),
        ("wave", "原檔、無轉碼",
         "ALAC 與 FLAC 不經重新編碼，從 CD 品質到高解析發行版本。播放器上的格式徽章告訴你此刻聽到的是什麼。"),
        ("lock", "隱私是架構，不是承諾",
         "你的 iPhone 直接連 Google，唯讀。Lossic 沒有伺服器——就算我們想看你的音樂庫，也無從看起。"),
        ("cloud", "離線是自然發生的",
         "播過的曲目留在手機裡。過隧道、上飛機，再播一次——完全不需要網路。"),
        ("grid", "專輯就該像專輯",
         "封面、作曲家、碟號——全部讀自你檔案裡的 tag。古典樂終於合理了：用作曲家瀏覽，而不是只有演奏者。"),
        ("box", "為真正的收藏而生",
         "CD 轉檔、Bandcamp 與 Qobuz 購買、現場錄音。這是你真正擁有的音樂庫——不是商店租給你的那個。"),
        ("book", "會講故事的播放器",
         "在播放畫面往右一滑，Lossic 就用 AI 介紹演奏者與這首曲子——素材來自檔案自己的 tag（用 Gemini 時還會參考專輯封面）。點一個推薦的追問，或打開「繼續問」聊下去。"),
        ("key", "你的金鑰，你的 AI",
         "自備 Gemini、OpenCode Zen 或 OpenRouter 的 API 金鑰；金鑰存在 iOS 鑰匙圈，App 直接連供應商。回答語言由你選：英文、繁中、簡中、日文、韓文。"),
    ],
    "how_title": "兩條路進來，零設定",
    "how_sub": "不用 NAS、不用 port forwarding、沒有伺服器要顧。",
    "steps": [
        ("你收藏的 CD", "放入 CD、接上 Mac，Lossic Mac App 自動幫你轉錄成 ALAC/FLAC，抓取專輯封面與曲目資訊自動寫入，再自動上傳到你 Google Drive 的 Lossic 目錄。幾分鐘後，iPhone 上直接無損播放，AI 隨時為你講解這張專輯。"),
        ("既有的 FLAC/ALAC 收藏", "已經有無損檔案？直接在手機上匯入——從 Google Drive 或任何 Files 位置選取一張專輯的檔案，它們就進到你自己的 Lossic 空間，馬上就能無損播放。"),
        ("然後，就只是聽", "專輯自動出現在封面牆。播過的曲目留在手機——網路斷了，音樂不斷。"),
    ],
    "privacy_title": "沒有帳號。沒有伺服器。沒有你音樂庫的副本。",
    "privacy_body": "多數雲端播放器會把你的檔案繞經它們自己的機器。Lossic 的後端是：沒有後端。你的檔案只走一段路——在 Google 與你的裝置之間，一條你隨時可以撤銷的連線。而且 Lossic 永遠只能看到它自己建立的檔案。",
    "faq_title": "常見問題",
    "faq": [
        ("Lossic 看得到我的音樂嗎？它們會經過誰的手？",
         "你的裝置直接連接 Google Drive——Lossic 沒有伺服器，任何東西都不會經過我們。轉錄或匯入的音樂，是從你的裝置直接上傳到你自己的 Drive。"),
        ("Lossic 能存取我 Google Drive 的所有內容嗎？",
         "不能——就算想也做不到。Lossic 使用 Google 權限最小的 <em>drive.file</em> 授權：只能存取 Lossic 自己建立或匯入的檔案，Lossic 目錄之外的一切對 app 完全不可見。這是 Google 在 API 層強制執行的，不是我們的口頭承諾。一個實際的影響：你 Drive 裡本來就有的 FLAC/ALAC，必須透過「匯入」功能重新匯入 Lossic 才能播放——直接在雲端把檔案複製進 Lossic 資料夾是沒有用的，因為可見性跟著「檔案由誰建立」走，不是跟著資料夾走。"),
        ("支援 iCloud 嗎？",
         "作為匯入來源——現在就支援：匯入的檔案選擇器裡就有 iCloud Drive，選了就會上傳到你的 Lossic 空間。作為儲存後端——還沒有，原因很誠實：iCloud 不給第三方 app 任何部分讀取的串流介面，播放一個只在雲端的檔案，等於要整個下載完才能出聲。Lossic 的瞬間播放（約 0.2 秒）、智慧快取、行動網路流量控制，全部建立在 Google Drive 的 HTTP 介面上。iCloud 後端未來可能以「便利選項」的形式加入，並誠實標示為「先同步、後播放」。"),
        ("支援 DSD 嗎？",
         "播放不支援——這是 Apple 的限制，不是我們的：iOS 沒有 DSD 解碼器，iPhone 硬體也無法原生播放 1 位元流。市面上號稱支援 DSD 的 app，實際上是播放時偷偷轉成 PCM——這跟一個講究位元誠實的產品格格不入。如果你有 DSD 收藏，建議用桌面工具一次性轉成 24-bit ALAC 或 FLAC 再匯入：品質良好的 DSD64 → 24/176.4 轉換在聽感上是透明的，而我們寧願你知情地轉一次，也不願在每次播放時替你偷偷轉。高解析 PCM（24/96、24/192）則原生支援，徽章如實顯示。"),
        ("支援哪些格式？",
         "ALAC 與 FLAC 是一等公民，另外支援 AAC 與 MP3。高解析檔案的格式會直接顯示在播放器上。"),
        ("串流會重新編碼我的檔案嗎？",
         "永遠不會。Lossic 用 HTTP range 請求串流檔案的原始位元組，途中不做轉碼。"),
        ("「秒開」到底多快？",
         "佇列中的專輯曲目通常約 0.2 秒出聲；第一次點播的新檔案在 Wi-Fi 上通常一秒內。這些是真實裝置量測的數字——對數字誠實，就是這個產品本身。"),
        ("為什麼是 Google Drive？",
         "因為儲存空間你已經付過錢了。Lossic 補上缺的那塊：一個把你的 Drive 當成本機音樂庫對待的播放器。"),
        ("「講故事」是怎麼運作的？",
         "在播放畫面往右一滑，Lossic 會請 AI 介紹演奏者與這首曲子，脈絡來自曲目內嵌的 tag——用 Gemini 時還包括專輯封面。畫面上有三個推薦的追問，一點就問；想聊更多就打開「繼續問」。"),
        ("需要訂閱 AI 嗎？我的隱私呢？",
         "金鑰自備——Gemini、OpenCode Zen 或 OpenRouter 都可以。金鑰存在 iOS 鑰匙圈，App 直接呼叫供應商，中間依然沒有 Lossic 的伺服器。用 Gemini 時可以選擇開啟 Google 搜尋 grounding，讓回答更新鮮。沒有金鑰？播放器一切照常——只是故事層不啟用。"),
        ("AI 會說錯嗎？",
         "會。這些介紹是生成的文字，可能有錯——把它當成一位懂音樂的朋友的說法，而不是工具書。相對地，播放速度的數字是實測的。"),
        ("什麼時候可以用？",
         "Lossic 正在密集開發中，目標是 App Store 上架。上架那天，這個頁面就會多出一顆下載按鈕。"),
    ],
    "cta_title": "把音樂重新變成你的。",
    "cta_button": "即將上架 App Store",
    "footer_note": "來自 <a href=\"https://foldic.app\">Foldic</a> 的開發者。",
    "footer_rights": "© 2026 Lossic",
    "legal_privacy": "隱私權政策", "legal_terms": "服務條款",
}

L["ja"] = {
    "lang_attr": "ja", "path": "/ja/", "dir": "ja",
    "font_body": '"Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Noto Sans JP", sans-serif',
    "font_head": '"Hiragino Mincho ProN", "Yu Mincho", "Noto Serif JP", serif',
    "line_height": "1.9", "letter_spacing": "0",
    "title": "Lossic — 音楽の物語を語るロスレスプレイヤー",
    "desc": "Lossic は ALAC と FLAC をあなた自身の Google Drive から直接ストリーミング。間にサーバーなし、再エンコードなし——タップから約0.2秒で再生。右にスワイプすれば、演奏者と曲の物語も。",
    "og_title": "Lossic",
    "og_desc": "あなたの音楽コレクションを、ポケットに。Drive のロスレス音源が即再生、アルバムの物語もスワイプひとつ。",
    "nav": ["機能", "仕組み", "よくある質問"],
    "support": "サポート",
    "h1": 'あなたのコレクションは、棚の上ではなく<br><em>ポケットの中に</em>',
    "sub": "あなた自身の Google Drive にあるロスレス音源が、タップした瞬間に鳴る——間にサーバーなし、再エンコードなし。Mac の Lossic Pro と合わせれば、CD を入れて数分後には iPhone で再生。ディスクからポケットまで、一本の流れ。",
    "badge": "開発中 · App Store 近日公開",
    "features_title": "あなたのライブラリのために。文字どおりに。",
    "features": [
        ("bolt", "即時再生",
         "タップして約0.2秒——キュー済みのアルバムトラックなら。実機と実ネットワークでの計測値です。宣伝文句ではありません。"),
        ("wave", "原音源のまま、再エンコードなし",
         "ALAC と FLAC を再エンコードせずストリーミング。CD 品質からハイレゾ音源まで、いま鳴っているフォーマットはバッジで確認できます。"),
        ("lock", "アーキテクチャによるプライバシー",
         "iPhone は Google と直接、読み取り専用で通信します。Lossic にはサーバーがありません——見ようと思っても、見る場所がないのです。"),
        ("cloud", "自然にオフライン",
         "再生したトラックは端末に残ります。トンネルでも機内でも、ネットワークゼロでもう一度。"),
        ("grid", "アルバムはアルバムらしく",
         "ジャケット、作曲家、ディスク番号——すべてファイル自身のタグから。クラシックがようやくまともに：演奏者だけでなく、作曲家で辿れます。"),
        ("box", "本物のコレクションのために",
         "CD リッピング、Bandcamp や Qobuz での購入、ライブ録音。ストアが貸してくれるものではなく、あなたが本当に所有するライブラリを。"),
        ("book", "物語を語るプレイヤー",
         "再生画面を右にスワイプすると、AI が演奏者とその曲を紹介します——素材はファイル自身のタグ（Gemini ならアルバムジャケットも）。提案された質問をタップするか、「もっと聞く」で会話を続けられます。"),
        ("key", "あなたのキーで、あなたの AI",
         "Gemini、OpenCode Zen、OpenRouter の API キーを自分で用意。キーは iOS のキーチェーンに保管され、アプリはプロバイダーと直接通信します。回答の言語は英語・繁体字中国語・簡体字中国語・日本語・韓国語から選べます。"),
    ],
    "how_title": "入り口はふたつ、設定なし",
    "how_sub": "NAS も、ポート開放も、面倒を見るサーバーもいりません。",
    "steps": [
        ("お手持ちの CD", "Mac の CD ドライブにディスクを入れるだけ。Lossic が ALAC/FLAC にリッピングし、ジャケットと曲情報を自動で書き込み、あなたの Google Drive の Lossic フォルダへ自動アップロード。数分後には iPhone でロスレス再生、AI がそのアルバムの物語を語ります。"),
        ("既存の FLAC/ALAC", "すでにロスレス音源をお持ちなら、iPhone から直接インポート。Google Drive や任意の「ファイル」の場所からアルバムのファイルを選ぶだけで、自分の Lossic スペースに入り、すぐ再生できます。"),
        ("あとは、聴くだけ", "アルバムはカバーウォールに自動で現れます。再生した曲は端末に残る——ネットワークが切れても、音楽は途切れません。"),
    ],
    "privacy_title": "アカウントなし。サーバーなし。ライブラリの複製なし。",
    "privacy_body": "多くのクラウドプレイヤーは、あなたのファイルを自社のマシン経由で流します。Lossic のバックエンドは「存在しない」。ファイルは Google とあなたの端末のあいだを、いつでも取り消せる接続で一区間だけ移動します。しかも Lossic に見えるのは、自身が作成したファイルだけです。",
    "faq_title": "よくある質問",
    "faq": [
        ("Lossic は私の音楽を見られますか？どこを経由しますか？",
         "端末が Google Drive と直接通信します。Lossic のサーバーは存在せず、何も私たちを経由しません。リッピングやインポートした音楽は、端末からあなた自身の Drive へ直接アップロードされます。"),
        ("Lossic は Google Drive の中身をすべて読めますか？",
         "いいえ——読みたくても読めません。Lossic は Google の最も限定された権限 <em>drive.file</em> を使用します。Lossic 自身が作成・インポートしたファイルにしかアクセスできず、それ以外は API レベルで完全に不可視です。これは Google が強制する仕組みであり、私たちの約束事ではありません。実際上の影響がひとつ：Drive に既にある FLAC/ALAC は、「インポート」機能で取り込む必要があります。Drive のウェブ画面で Lossic フォルダにコピーしても読めません——可視性は「どのアプリが作成したか」に紐づき、フォルダには紐づかないためです。"),
        ("iCloud には対応していますか？",
         "インポート元としては——今日から使えます。インポートのファイル選択には iCloud Drive も表示され、選んだファイルは Lossic のスペースにアップロードされます。保存先としては——まだです。理由は正直に：iCloud はサードパーティアプリに部分読み込みのストリーミング手段を提供しないため、クラウドのみのファイルは丸ごとダウンロードし終えるまで音が出ません。Lossic の瞬間再生（約0.2秒）、スマートキャッシュ、モバイル通信量の制御は、すべて Google Drive の HTTP インターフェイスの上に成り立っています。iCloud バックエンドは将来、「同期してから再生」と明示した利便性オプションとして追加されるかもしれません。"),
        ("DSD には対応していますか？",
         "再生には対応していません——これは Apple の制約であって、私たちの怠慢ではありません。iOS に DSD デコーダはなく、iPhone のハードウェアは 1 ビットストリームをネイティブ再生できません。「DSD 対応」を謳うアプリは、実際には再生時にこっそり PCM へ変換しています——ビットへの誠実さを掲げる製品には合いません。DSD コレクションをお持ちなら、デスクトップツールで一度だけ 24-bit ALAC/FLAC に変換してからインポートしてください。良質な DSD64 → 24/176.4 変換は聴感上透明です。毎回の再生で黙って変換するより、一度だけ、知った上で変換するほうが誠実だと考えます。ハイレゾ PCM（24/96、24/192）はネイティブ対応で、バッジも正直に表示されます。"),
        ("対応フォーマットは？",
         "ALAC と FLAC を第一級として、AAC と MP3 にも対応。ハイレゾ音源のフォーマットはプレイヤーに表示されます。"),
        ("ストリーミングで再エンコードされますか？",
         "決してされません。HTTP レンジリクエストでファイルの元のバイトを送り、途中でトランスコードしません。"),
        ("「一瞬」とは、どれくらい？",
         "キュー済みのアルバムトラックで約0.2秒。新しいファイルへのコールドタップは Wi-Fi でおおむね1秒以内。実機での計測値であり、この数字に正直であることが製品そのものです。"),
        ("なぜ Google Drive？",
         "ストレージ代はもう払っているからです。Lossic は欠けていた部分——Drive をローカルライブラリのように扱うプレイヤー——を足すだけです。"),
        ("「物語」機能はどう動くのですか？",
         "再生画面を右にスワイプすると、Lossic が AI に演奏者とその曲の紹介を頼みます。文脈はトラックに埋め込まれたタグから——Gemini の場合はアルバムジャケットも使います。提案された3つの質問はワンタップ、「もっと聞く」を開けば再生中の曲について会話を続けられます。"),
        ("AI のサブスクリプションは必要？プライバシーは？",
         "API キーはご自身で用意します——Gemini、OpenCode Zen、OpenRouter のいずれか。キーは iOS のキーチェーンに保管され、アプリはプロバイダーと直接通信します。ここにも Lossic のサーバーは存在しません。Gemini では Google 検索グラウンディングをオプトインで有効にできます。キーがなければ？プレイヤーは何も変わらず動きます——物語のレイヤーが休んでいるだけです。"),
        ("AI は間違えますか？",
         "はい。紹介文は生成されたテキストであり、誤りを含むことがあります。事典ではなく、音楽に詳しい友人の語りとして受け取ってください。一方、再生速度の数字は実測値です。"),
        ("いつ使えますか？",
         "Lossic は鋭意開発中で、App Store を目指しています。公開の日、このページにダウンロードボタンが現れます。"),
    ],
    "cta_title": "音楽を、もう一度自分のものに。",
    "cta_button": "App Store 近日公開",
    "footer_note": "<a href=\"https://foldic.app\">Foldic</a> の開発者より。",
    "footer_rights": "© 2026 Lossic",
    "legal_privacy": "プライバシー", "legal_terms": "利用規約",
}

L["ko"] = {
    "lang_attr": "ko", "path": "/ko/", "dir": "ko",
    "font_body": '"Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", sans-serif',
    "font_head": '"Apple SD Gothic Neo", "Noto Sans KR", sans-serif',
    "head_weight": "800",
    "line_height": "1.8", "letter_spacing": "-0.01em",
    "title": "Lossic — 음악의 이야기를 들려주는 무손실 플레이어",
    "desc": "Lossic은 ALAC과 FLAC을 내 Google Drive에서 바로 스트리밍합니다. 중간 서버 없음, 재인코딩 없음 — 탭 후 약 0.2초 만에 재생. 오른쪽으로 스와이프하면 연주자와 곡의 이야기까지.",
    "og_title": "Lossic",
    "og_desc": "내 음악 컬렉션을 주머니 속에 — 내 Drive의 무손실 음악이 즉시 재생되고, 앨범의 이야기는 스와이프 한 번에.",
    "nav": ["기능", "작동 방식", "자주 묻는 질문"],
    "support": "지원",
    "h1": '내 음악 컬렉션은 선반이 아니라<br><em>주머니 속에 있습니다</em>',
    "sub": "내 Google Drive의 무손실 음악이 탭하는 순간 재생됩니다 — 중간 서버 없음, 재인코딩 없음. Mac용 Lossic Pro와 함께라면 CD를 넣고 몇 분 뒤 iPhone에서 바로 재생. 디스크에서 주머니까지, 하나의 파이프라인.",
    "badge": "개발 중 · App Store 출시 예정",
    "features_title": "내 라이브러리답게 만들었습니다. 실제로 내 것이니까요.",
    "features": [
        ("bolt", "즉시 재생",
         "탭하면 바로 재생 — 큐에 있는 앨범 트랙은 약 0.2초. 실제 기기와 실제 네트워크에서 측정한 숫자입니다."),
        ("wave", "원본 그대로, 재인코딩 없이",
         "ALAC과 FLAC을 재인코딩 없이 스트리밍합니다. CD 음질부터 고해상도 음원까지, 지금 듣는 포맷이 배지로 표시됩니다."),
        ("lock", "아키텍처가 곧 프라이버시",
         "iPhone이 Google과 직접, 읽기 전용으로 통신합니다. Lossic에는 서버가 없습니다 — 보고 싶어도 볼 곳이 없습니다."),
        ("cloud", "자연스러운 오프라인",
         "재생한 트랙은 기기에 남습니다. 터널에서도, 비행기에서도, 네트워크 없이 다시 재생하세요."),
        ("grid", "앨범다운 앨범",
         "커버, 작곡가, 디스크 번호 — 모두 파일 자체의 태그에서 읽습니다. 클래식도 드디어 제대로: 연주자만이 아니라 작곡가로 탐색합니다."),
        ("box", "진짜 컬렉션을 위해",
         "CD 립, Bandcamp와 Qobuz 구매, 라이브 녹음. 스토어가 빌려주는 라이브러리가 아니라, 내가 실제로 소유한 라이브러리."),
        ("book", "이야기를 들려주는 플레이어",
         "재생 화면에서 오른쪽으로 스와이프하면 AI가 연주자와 이 곡을 소개합니다 — 재료는 파일 자체의 태그(Gemini에서는 앨범 커버까지). 추천 질문을 탭하거나 '더 묻기'를 열어 대화를 이어가세요."),
        ("key", "내 키로, 내 AI",
         "Gemini, OpenCode Zen, OpenRouter의 API 키를 직접 가져옵니다. 키는 iOS 키체인에 보관되고 앱이 제공자와 직접 통신합니다. 답변 언어는 영어·번체 중국어·간체 중국어·일본어·한국어 중에서 선택할 수 있습니다."),
    ],
    "how_title": "들어오는 길은 두 가지, 설정 없음",
    "how_sub": "NAS도, 포트 포워딩도, 돌봐야 할 서버도 없습니다.",
    "steps": [
        ("내 CD 컬렉션", "Mac의 CD 드라이브에 디스크를 넣기만 하세요. Lossic이 ALAC/FLAC으로 리핑하고 앨범 아트와 곡 정보를 자동으로 기록해 내 Google Drive의 Lossic 폴더로 자동 업로드합니다. 몇 분 뒤 iPhone에서 무손실로 재생되고, AI가 그 앨범의 이야기를 들려줍니다."),
        ("기존 FLAC/ALAC 컬렉션", "이미 무손실 파일이 있다면 iPhone에서 바로 가져오세요. Google Drive나 파일 앱의 어느 위치에서든 앨범 파일을 선택하면 내 Lossic 공간으로 들어와 즉시 재생됩니다."),
        ("그다음은, 그냥 듣기", "앨범은 커버 월에 자동으로 나타납니다. 재생한 곡은 기기에 남아 — 네트워크가 끊겨도 음악은 계속됩니다."),
    ],
    "privacy_title": "계정 없음. 서버 없음. 라이브러리 사본 없음.",
    "privacy_body": "대부분의 클라우드 플레이어는 파일을 자사 서버를 거쳐 보냅니다. Lossic의 백엔드는 '없음'입니다. 파일은 Google과 내 기기 사이 단 한 구간만 이동하며, 언제든 취소할 수 있는 연결을 사용합니다. 그리고 Lossic은 자신이 만든 파일만 볼 수 있습니다.",
    "faq_title": "자주 묻는 질문",
    "faq": [
        ("Lossic이 내 음악을 볼 수 있나요? 어디를 거치나요?",
         "기기가 Google Drive와 직접 통신합니다. Lossic 서버는 존재하지 않으며 아무것도 저희를 거치지 않습니다. 리핑하거나 가져온 음악은 기기에서 내 Drive로 직접 업로드됩니다."),
        ("Lossic이 내 Google Drive 전체에 접근할 수 있나요?",
         "아니요 — 원해도 불가능합니다. Lossic은 Google의 가장 제한적인 권한인 <em>drive.file</em>을 사용합니다. Lossic이 직접 생성하거나 가져온 파일만 볼 수 있고, 그 외의 모든 것은 API 차원에서 완전히 보이지 않습니다. 이는 Google이 강제하는 구조이지 저희의 약속이 아닙니다. 실질적인 영향 하나: Drive에 이미 있는 FLAC/ALAC은 '가져오기' 기능으로 다시 가져와야 합니다. Drive 웹에서 Lossic 폴더로 복사해도 재생할 수 없습니다 — 가시성은 폴더가 아니라 '파일을 만든 앱'을 따라가기 때문입니다."),
        ("iCloud를 지원하나요?",
         "가져오기 소스로는 — 지금 바로 됩니다. 가져오기 파일 선택기에 iCloud Drive가 표시되며, 선택한 파일은 내 Lossic 공간으로 업로드됩니다. 저장 백엔드로는 — 아직입니다. 이유는 정직하게: iCloud는 서드파티 앱에 부분 읽기 스트리밍 인터페이스를 제공하지 않아, 클라우드에만 있는 파일은 전체를 내려받아야 소리가 납니다. Lossic의 즉시 재생(약 0.2초), 스마트 캐시, 셀룰러 데이터 제어는 모두 Google Drive의 HTTP 인터페이스 위에 서 있습니다. iCloud 백엔드는 훗날 '동기화 후 재생'임을 명시한 편의 옵션으로 추가될 수 있습니다."),
        ("DSD를 지원하나요?",
         "재생은 지원하지 않습니다 — 이는 Apple의 제약이지 저희 탓이 아닙니다. iOS에는 DSD 디코더가 없고 iPhone 하드웨어는 1비트 스트림을 네이티브로 재생할 수 없습니다. 'DSD 지원'을 내세우는 앱들은 실제로는 재생 시 몰래 PCM으로 변환합니다 — 비트 정직함을 내세우는 제품과는 맞지 않습니다. DSD 컬렉션이 있다면 데스크톱 도구로 한 번만 24-bit ALAC/FLAC으로 변환해 가져오세요. 잘 된 DSD64 → 24/176.4 변환은 청감상 투명하며, 재생 때마다 몰래 변환하는 것보다 알고서 한 번 변환하는 편이 정직하다고 믿습니다. 하이레즈 PCM(24/96, 24/192)은 네이티브로 재생되며 배지도 정직하게 표시됩니다."),
        ("어떤 포맷을 지원하나요?",
         "ALAC과 FLAC을 최우선으로, AAC와 MP3도 지원합니다. 고해상도 음원의 포맷은 플레이어에 표시됩니다."),
        ("스트리밍하면 재인코딩되나요?",
         "절대 아닙니다. HTTP 레인지 요청으로 파일의 원본 바이트를 보내며, 중간에 트랜스코딩하지 않습니다."),
        ("'즉시'는 얼마나 빠른가요?",
         "큐에 있는 앨범 트랙은 약 0.2초, 새 파일의 첫 재생은 Wi-Fi에서 보통 1초 이내입니다. 실제 기기에서 측정한 숫자이며, 이 숫자에 정직한 것이 곧 이 제품입니다."),
        ("왜 Google Drive인가요?",
         "저장 공간 비용은 이미 내고 계시니까요. Lossic은 빠져 있던 조각 — Drive를 로컬 라이브러리처럼 다루는 플레이어 — 를 더할 뿐입니다."),
        ("'이야기' 기능은 어떻게 작동하나요?",
         "재생 화면에서 오른쪽으로 스와이프하면 Lossic이 AI에게 연주자와 이 곡의 소개를 요청합니다. 맥락은 트랙에 내장된 태그에서 — Gemini의 경우 앨범 커버도 함께 사용합니다. 추천 질문 세 개는 탭 한 번, '더 묻기'를 열면 지금 재생 중인 곡에 대해 대화를 이어갈 수 있습니다."),
        ("AI 구독이 필요한가요? 프라이버시는요?",
         "API 키는 직접 준비합니다 — Gemini, OpenCode Zen, OpenRouter 중 선택. 키는 iOS 키체인에 보관되고 앱이 제공자를 직접 호출하며, 여기에도 Lossic 서버는 없습니다. Gemini에서는 Google 검색 그라운딩을 선택적으로 켤 수 있습니다. 키가 없다면? 플레이어는 똑같이 작동합니다 — 이야기 레이어만 꺼져 있을 뿐입니다."),
        ("AI가 틀릴 수도 있나요?",
         "네. 소개문은 생성된 텍스트라 오류가 있을 수 있습니다. 백과사전이 아니라 음악을 잘 아는 친구의 이야기로 받아들여 주세요. 반면 재생 속도 숫자는 실측값입니다."),
        ("언제 쓸 수 있나요?",
         "Lossic은 개발 중이며 App Store 출시를 목표로 하고 있습니다. 출시되는 날 이 페이지에 다운로드 버튼이 생깁니다."),
    ],
    "cta_title": "음악을 다시 내 것으로.",
    "cta_button": "App Store 출시 예정",
    "footer_note": "<a href=\"https://foldic.app\">Foldic</a> 개발자가 만듭니다.",
    "footer_rights": "© 2026 Lossic",
    "legal_privacy": "개인정보처리방침", "legal_terms": "이용약관",
}

ICONS = {
    "bolt": '<svg viewBox="0 0 24 24"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z"/></svg>',
    "wave": '<svg viewBox="0 0 24 24"><path d="M3 12h2M7 8v8M11 4v16M15 7v10M19 10v4"/></svg>',
    "lock": '<svg viewBox="0 0 24 24"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>',
    "cloud": '<svg viewBox="0 0 24 24"><path d="M6 18a4 4 0 0 1 0-8 6 6 0 0 1 11.3-1.9A4.5 4.5 0 0 1 17 18H6z"/><path d="M12 12v6M9.5 15.5 12 18l2.5-2.5"/></svg>',
    "grid": '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="8" height="8" rx="1.5"/><rect x="13" y="3" width="8" height="8" rx="1.5"/><rect x="3" y="13" width="8" height="8" rx="1.5"/><rect x="13" y="13" width="8" height="8" rx="1.5"/></svg>',
    "box": '<svg viewBox="0 0 24 24"><path d="M3 7 12 3l9 4-9 4-9-4z"/><path d="M3 7v10l9 4 9-4V7"/><path d="M12 11v10"/></svg>',
    "book": '<svg viewBox="0 0 24 24"><path d="M12 6c-1.5-1.6-3.6-2-6-2H4v14h2c2.4 0 4.5.4 6 2 1.5-1.6 3.6-2 6-2h2V4h-2c-2.4 0-4.5.4-6 2z"/><path d="M12 6v14"/></svg>',
    "key": '<svg viewBox="0 0 24 24"><circle cx="8" cy="14" r="4"/><path d="M11 11 20 2"/><path d="M16 6l3 3"/><path d="M13 9l2 2"/></svg>',
}

HREFLANGS = """  <link rel="alternate" hreflang="en" href="https://lossic.app/">
  <link rel="alternate" hreflang="zh-Hant" href="https://lossic.app/zh/">
  <link rel="alternate" hreflang="ja" href="https://lossic.app/ja/">
  <link rel="alternate" hreflang="ko" href="https://lossic.app/ko/">
  <link rel="alternate" hreflang="x-default" href="https://lossic.app/">"""

# First-visit locale routing, root page only. An explicit choice (stored on
# click) and ?lang=en both win, so nobody gets trapped — foldic's pattern.
ROUTER = """  <script>
    document.addEventListener("click", function (event) {
      var link = event.target.closest(".lang a");
      if (!link) return;
      try { localStorage.setItem("lossic-lang", link.getAttribute("href")); } catch (e) {}
    });
  </script>
  <script>
    (function () {
      var params = new URLSearchParams(location.search);
      if (params.get("lang") === "en") return;
      var saved = null;
      try { saved = localStorage.getItem("lossic-lang"); } catch (e) {}
      if (saved) {
        if (saved !== "/") location.replace(saved);
        return;
      }
      var map = [[/^zh/i, "/zh/"], [/^ja/i, "/ja/"], [/^ko/i, "/ko/"]];
      var langs = navigator.languages && navigator.languages.length
        ? navigator.languages : [navigator.language || ""];
      for (var i = 0; i < langs.length; i++) {
        for (var j = 0; j < map.length; j++) {
          if (map[j][0].test(langs[i])) { location.replace(map[j][1]); return; }
        }
        if (/^en/i.test(langs[i])) return;
      }
    })();
  </script>"""

REMEMBER = """  <script>
    document.addEventListener("click", function (event) {
      var link = event.target.closest(".lang a");
      if (!link) return;
      try { localStorage.setItem("lossic-lang", link.getAttribute("href")); } catch (e) {}
    });
  </script>"""


def lang_switcher(current):
    parts = []
    for code, label in [("zh", "中文"), ("ja", "日本語"), ("ko", "한국어"), ("en", "EN")]:
        href = "/" if code == "en" else f"/{code}/"
        # ?lang=en so the router does not bounce an explicit EN choice back.
        if code == "en":
            href = "/?lang=en"
        cls = ' class="active"' if code == current else ""
        parts.append(f'<a{cls} href="{href}">{label}</a>')
    return "|".join(parts)


def page(code):
    t = L[code]
    feats = "\n".join(
        f'''      <div class="feature">
        <div class="icon">{ICONS[icon]}</div>
        <h3>{title}</h3>
        <p>{body}</p>
      </div>''' for icon, title, body in t["features"])
    steps = "\n".join(
        f'''        <div class="step"><div class="num">{i}</div><h3>{title}</h3><p>{body}</p></div>'''
        for i, (title, body) in enumerate(t["steps"], 1))
    faqs = "\n".join(
        f'''      <details>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>''' for q, a in t["faq"])
    nav_ids = ["#features", "#how", "#faq"]
    nav = "\n      ".join(
        f'<a href="{nav_ids[i]}">{label}</a>' for i, label in enumerate(t["nav"]))
    if code == "zh":
        # Only zh has a pricing page for now.
        nav += '\n      <a href="/zh/pricing/">價格</a>'
    og_url = "https://lossic.app" + t["path"]

    return f'''<!DOCTYPE html>
<html lang="{t["lang_attr"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t["title"]}</title>
  <meta name="description" content="{t["desc"]}">
  <meta name="google-site-verification" content="SDpa7qNwmvsPvoiA6yq-NlIMMDP5biqjUsmwtVVfZ14" />
  <meta property="og:title" content="{t["og_title"]}">
  <meta property="og:description" content="{t["og_desc"]}">
  <meta property="og:image" content="https://lossic.app/og.png">
  <meta property="og:url" content="{og_url}">
{HREFLANGS}
  <link rel="icon" type="image/png" href="/icon.png">
  <link rel="shortcut icon" href="/favicon.ico">
  <style>
    :root {{
      --sage: #A8B394;
      --sage-deep: #4A5340;
      --sage-tint: #E7EADD;
      --ink: #333B2B;
      --muted: #757D66;
      --bg: #F6F5EE;
      --card: #EFEEE2;
      --border: rgba(74, 83, 64, 0.16);
      --shadow: 0 24px 80px rgba(51, 59, 43, 0.2);
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --sage: #A8B394;
        --sage-deep: #C2CCA9;
        --sage-tint: #2B3123;
        --ink: #ECEEE1;
        --muted: #A6AD93;
        --bg: #181B12;
        --card: #21261A;
        --border: rgba(168, 179, 148, 0.2);
        --shadow: 0 24px 80px rgba(0, 0, 0, 0.55);
      }}
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: {t["font_body"]};
      color: var(--ink);
      background: var(--bg);
      line-height: {t["line_height"]};
      -webkit-font-smoothing: antialiased;
    }}

    nav {{
      position: sticky; top: 0; z-index: 10;
      display: flex; align-items: center; justify-content: space-between;
      max-width: 1080px; margin: 0 auto; padding: 0.9rem 1.5rem;
      backdrop-filter: saturate(180%) blur(16px);
    }}
    nav .brand {{ display: flex; align-items: center; gap: 0.55rem; font-weight: 700; font-size: 1.05rem; text-decoration: none; color: var(--ink); }}
    nav .brand img {{ width: 28px; height: 28px; border-radius: 7px; }}
    nav .links {{ display: flex; align-items: center; flex-wrap: wrap; }}
    nav .links a {{ color: var(--muted); text-decoration: none; margin-left: 1.4rem; font-size: 0.92rem; }}
    nav .links a:hover {{ color: var(--sage-deep); }}
    nav .lang {{ margin-left: 1.4rem; font-size: 0.9rem; color: var(--muted); }}
    nav .lang a {{ margin: 0 0.15rem; text-decoration: none; color: var(--muted); }}
    nav .lang a.active {{ color: var(--ink); font-weight: 700; }}
    @media (max-width: 720px) {{
      nav {{ flex-direction: column; gap: 0.45rem; padding: 0.7rem 1rem 0.65rem; }}
      nav .links {{ justify-content: center; gap: 0.2rem 1rem; }}
      nav .links a {{ margin-left: 0; font-size: 0.86rem; }}
      nav .lang {{ margin-left: 0; }}
      .hero {{ padding-top: 2.6rem; }}
    }}

    .hero {{
      max-width: 1080px; margin: 0 auto; padding: 4.2rem 1.5rem 0;
      text-align: center;
    }}
    .hero .app-icon {{
      width: 108px; height: 108px; border-radius: 24px;
      box-shadow: 0 12px 36px rgba(51, 59, 43, 0.25);
      margin-bottom: 1.6rem;
    }}
    .hero h1 {{
      font-family: {t["font_head"]};
      font-size: clamp(2.2rem, 6vw, 3.4rem);
      line-height: 1.18;
      letter-spacing: {t["letter_spacing"]};
      font-weight: {t.get("head_weight", "700")};
      max-width: 820px; margin: 0 auto;
    }}
    .hero h1 em {{
      font-style: normal;
      background: linear-gradient(transparent 58%, rgba(168, 179, 148, 0.55) 58%, rgba(168, 179, 148, 0.55) 94%, transparent 94%);
      padding: 0 0.06em;
    }}
    .hero p.sub {{
      color: var(--muted); font-size: 1.16rem; max-width: 700px;
      margin: 1.2rem auto 0;
    }}
    .badge {{
      display: inline-flex; align-items: center; gap: 0.45rem;
      margin-top: 1.8rem;
      font-size: 0.88rem; font-weight: 600; color: var(--sage-deep);
      background: var(--sage-tint); border: 1px solid var(--border);
      padding: 0.45rem 1rem; border-radius: 999px;
    }}
    .badge::before {{
      content: ""; width: 8px; height: 8px; border-radius: 50%;
      background: var(--sage); animation: pulse 2.4s ease-in-out infinite;
    }}
    @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.35; }} }}

    section.features {{ max-width: 1080px; margin: 0 auto; padding: 4.6rem 1.5rem 1rem; }}
    h2.section-title {{ font-family: {t["font_head"]}; font-size: 1.9rem; letter-spacing: {t["letter_spacing"]}; margin-bottom: 1.6rem; text-align: center; }}
    .features-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.1rem;
    }}
    .feature {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 1.6rem;
    }}
    .feature .icon {{
      width: 42px; height: 42px; border-radius: 11px;
      background: var(--sage-tint);
      display: flex; align-items: center; justify-content: center;
      margin-bottom: 0.9rem;
    }}
    .feature .icon svg {{ width: 22px; height: 22px; stroke: var(--sage-deep); fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
    .feature h3 {{ font-size: 1.04rem; margin-bottom: 0.35rem; }}
    .feature p {{ font-size: 0.94rem; color: var(--muted); }}

    section.how {{ max-width: 880px; margin: 0 auto; padding: 4.2rem 1.5rem 1rem; text-align: center; }}
    p.section-sub {{ color: var(--muted); max-width: 560px; margin: -0.8rem auto 2.4rem; }}
    .steps {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.6rem; text-align: left; }}
    .step .num {{
      font-size: 0.8rem; font-weight: 700; color: var(--sage-deep);
      background: var(--sage-tint); border-radius: 999px;
      width: 26px; height: 26px; display: flex; align-items: center; justify-content: center;
      margin-bottom: 0.7rem;
    }}
    .step h3 {{ font-size: 1rem; margin-bottom: 0.3rem; }}
    .step p {{ font-size: 0.92rem; color: var(--muted); }}

    section.privacy {{
      max-width: 780px; margin: 4.2rem auto 0; padding: 0 1.5rem;
    }}
    .privacy-card {{
      background: var(--sage-tint); border: 1px solid var(--border);
      border-radius: 20px; padding: 2.2rem; text-align: center;
    }}
    .privacy-card h2 {{ font-family: {t["font_head"]}; font-size: 1.5rem; letter-spacing: {t["letter_spacing"]}; margin-bottom: 0.7rem; }}
    .privacy-card p {{ color: var(--muted); font-size: 0.98rem; max-width: 620px; margin: 0 auto; }}

    section.faq {{ max-width: 720px; margin: 0 auto; padding: 4.2rem 1.5rem 2rem; }}
    .faq details {{ border-bottom: 1px solid var(--border); padding: 1rem 0.2rem; }}
    .faq summary {{ cursor: pointer; font-weight: 600; font-size: 1rem; list-style: none; display: flex; justify-content: space-between; align-items: center; gap: 0.6rem; }}
    .faq summary::after {{ content: "+"; color: var(--sage-deep); font-size: 1.3rem; font-weight: 400; flex-shrink: 0; }}
    .faq details[open] summary::after {{ content: "–"; }}
    .faq details p {{ color: var(--muted); font-size: 0.95rem; padding-top: 0.6rem; }}

    .bottom-cta {{
      text-align: center; padding: 4.5rem 1.5rem;
      background: linear-gradient(180deg, transparent, var(--sage-tint));
    }}
    .bottom-cta h2 {{ font-family: {t["font_head"]}; font-size: 1.8rem; letter-spacing: {t["letter_spacing"]}; margin-bottom: 1.4rem; }}
    .cta.pending {{
      display: inline-flex; align-items: center; gap: 0.5rem;
      background: transparent; color: var(--muted);
      border: 1.5px dashed var(--border); border-radius: 12px;
      padding: 0.85rem 1.5rem; font-weight: 600; font-size: 0.98rem;
      cursor: default; text-decoration: none;
    }}

    footer {{
      border-top: 1px solid var(--border);
      padding: 2.2rem 1.5rem; text-align: center;
      color: var(--muted); font-size: 0.88rem;
    }}
    footer a {{ color: var(--sage-deep); text-decoration: none; margin: 0 0.2rem; }}
  </style>
{ROUTER if code == "en" else REMEMBER}
</head>
<body>
  <nav>
    <a class="brand" href="{t["path"]}"><img src="/icon.png" alt="" width="28" height="28">Lossic</a>
    <div class="links">
      {nav}
      <a href="mailto:tautiu.dev+lossic@gmail.com">{t["support"]}</a>
      <span class="lang">{lang_switcher(code)}</span>
    </div>
  </nav>

  <header class="hero">
    <img class="app-icon" src="/icon.png" alt="Lossic app icon" width="108" height="108">
    <h1>{t["h1"]}</h1>
    <p class="sub">{t["sub"]}</p>
    <div class="badge">{t["badge"]}</div>
  </header>

  <section class="features" id="features">
    <h2 class="section-title">{t["features_title"]}</h2>
    <div class="features-grid">
{feats}
    </div>
  </section>

  <section class="how" id="how">
    <h2 class="section-title">{t["how_title"]}</h2>
    <p class="section-sub">{t["how_sub"]}</p>
    <div class="steps">
{steps}
    </div>
  </section>

  <section class="privacy">
    <div class="privacy-card">
      <h2>{t["privacy_title"]}</h2>
      <p>{t["privacy_body"]}</p>
    </div>
  </section>

  <section class="faq" id="faq">
    <h2 class="section-title">{t["faq_title"]}</h2>
{faqs}
  </section>

  <div class="bottom-cta">
    <h2>{t["cta_title"]}</h2>
    <span class="cta pending">{t["cta_button"]}</span>
  </div>

  <footer>
    <div>{t["footer_note"]}</div>
    <div><a href="/privacy/">{t["legal_privacy"]}</a> · <a href="/terms/">{t["legal_terms"]}</a></div>
    <div>{t["footer_rights"]}</div>
  </footer>
</body>
</html>
'''


def main():
    for code, t in L.items():
        out_dir = os.path.join(SITE, t["dir"]) if t["dir"] else SITE
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "index.html")
        html = page(code)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"{path}  {len(html.splitlines())} lines")


if __name__ == "__main__":
    main()
