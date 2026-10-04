# you asked

message time: 2026-08-13 12:42:58

這樣的話，其實用cua 理論上是最佳，因為有啥問題fabric都會叫hgk去升級修補，不是嗎

---

# chatgpt response

對，**以你目前已完成的 Fabric → HGK → Hermes 架構來看，Cua 很可能就是最合理的 P0 預設選型。**

原因不是「Cua一定比 UFO²強」，而是整個系統已經具備一個很重要的補償機制：

```text
Cua 出問題
→ Fabric 偵測 capability / acceptance 缺口
→ HGK 產生受控修補 WorkOrder
→ Hermes / Codex 修 adapter、binding、wrapper、fixture
→ affected regression
→ Acceptance Officer 驗證
→ promotion / rollback
```

RP-002 Stage-2本來就要求正常自托管路徑收斂成：

```text
WorkOrder
→ ExecutionBinding
→ Profile
→ Kanban/Hermes
```

並且工具、Profile、provider的問題要走現有 capability lifecycle，而不是再造第二套 runtime。

因此，**Cua 的最大優勢其實是「低整合成本 + 問題可被你現有 Fabric/HGK repair loop 吸收」**。

---

## 但要補一個關鍵限制

不能把它理解成：

> 「Cua什麼問題 Fabric/HGK 都一定修得掉。」

更精確是：

### HGK 能修的

例如：

- Hermes ↔ Cua wrapper不相容；
- Windows selector/UIA mapping；
- XQ-specific adapter；
- dialog recovery；
- retry/readback；
- permission manifest；
- provider binding；
- version pin；
- installer；
- timeout/reclaim；
- fixtures/tests；
- XQ version drift；
- UI workflow變更。

這些都很適合：

```text
Fabric finding
→ HGK governed repair
```

---

### HGK 不一定能「修掉」的

例如 Cua upstream本身存在：

```text
Windows driver fundamental defect
OS/UIPI limitation
XQ custom control完全不可觀測
upstream regression
binary crash
第三方license/compatibility問題
```

這種情況 HGK合理行為不是永遠硬修 Cua，而是：

```text
detect
→ isolate
→ pin / rollback
→ workaround
→ upstream issue/patch
→ switch provider
```

這正是為什麼 Fabric最好管理：

```text
Capability = WINDOWS_DESKTOP_AUTOMATION
```

而不是把架構寫死成：

```text
Capability = CUA
```

Master本身就要求工具能力要保留 qualification、fallback、rollback、anti-downgrade，而不能用工具名稱取代authority。

---

# 所以最合理的實際配置

我現在會推薦：

```yaml
capability: WINDOWS_DESKTOP_AUTOMATION

profile:
  fabric-desktop-automation

provider:
  primary: CUA_DRIVER
  standby: NONE_INITIAL
```

一開始**甚至不用先裝 UFO²**。

先讓：

```text
Hermes
→ native computer_use
→ Cua
→ XQ
```

跑真實 qualification。

如果穩：

```text
CUA = ACTIVE_PRIMARY
UFO² = DEFERRED
```

就到此為止。

這才是最低磨合、最快落地、最不過度工程化。

---

## 只有 Cua 出現「HGK修補仍無法合理解決」的能力缺口

例如：

```text
XQ custom control
→ repeated Cua failure
→ HGK adapter repair
→ still failure
```

才啟動：

```text
FIT_GAP
→ UFO² qualification
```

然後可能變成：

```text
CUA = ACTIVE_PRIMARY
UFO² = QUALIFIED_FALLBACK
```

或者如果 UFO²實測全面更好：

```text
UFO² = ACTIVE_PRIMARY
CUA = STANDBY
```

Fabric/HGK正好負責這種 provider lifecycle。

---

# 更重要的是：Fabric完成後，「初始工具完美」的重要性下降了

這其實就是你抓到的重點。

在沒有Fabric/HGK evolution能力的普通系統裡，你會非常在意：

> 「第一次選的 automation tool是不是最強？」

因為選錯後維護很痛苦。

但你現在的架構是：

```text
Tool
↓
Capability qualification
↓
runtime evidence
↓
drift detection
↓
governed repair
↓
requalification
↓
promotion / rollback
```

Stage-3甚至明確要求工具/provider不能 silent fallback，current route要有digest與anti-downgrade。

所以選型策略可以改成：

> **先選與現有系統摩擦最低、足夠好的工具，再讓 Fabric/HGK 用實際缺陷驅動演進。**

這比一開始花大量時間尋找「理論上最完美 GUI Agent」更符合你的系統。

---

# 我的最終排序因此再收斂

### P0

**Hermes Computer Use + Cua Driver**

理由：

```text
Hermes native fit
+
少一層adapter
+
Fabric可治理
+
HGK可修補
+
可rollback/requalify
+
快速開始XQ實測
```

### P1

**UFO²**

只在真實 XQ evidence證明：

```text
CUA_NO_FIT
```

或：

```text
UFO² materially better
```

時才導入。

### P2

OpenAdapt等：

只有當某些XQ workflow已高度穩定、值得compile成deterministic replay時再考慮。

---

## 一句話總結

**是，你的理解基本正確。**

在目前 Fabric-governed 架構下：

> **Cua 不必是世界上功能最強的 desktop automation framework；它只需要是「最容易接入 Hermes、足夠可靠，而且其缺陷能被 Fabric → HGK 的受治理修補迴圈有效吸收」的那個工具。**

以這個標準，我目前會把 **Cua 定為第一順位正式施工候選**，而不是先把 UFO²一起導入。

唯一要保留的安全閥就是：

> **Fabric綁定的是 `WINDOWS_DESKTOP_AUTOMATION` capability，不是永遠綁死 `CUA_DRIVER` provider。**

這樣你同時拿到**最低磨合**和**未來可替換性**。

---
Powered by [AI Exporter](https://saveai.net)