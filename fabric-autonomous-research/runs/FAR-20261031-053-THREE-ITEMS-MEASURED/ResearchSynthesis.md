# FAR-053｜O-1 不是「等你簽一個危險的 graft」，是「兩個不同的樹」

日期：2026-11-01（台北）
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`

---

## 0. 三件事，三種不同的性質

| 項 | 我原本的講法 | 查證後 | 性質 |
|---|---|---|---|
| **D-H** 憑證輪替 | 「輪替仍是你的步驟」 | 該檔**從未被 commit**（`git log --all` 零筆），且**已在 `.gitignore`** | **預防性**，不是洩漏 |
| **O-2** fast-forward | 「你一鍵」 | `merge/epoch-40-ff-20261101` 相對 `origin/main`：**4 ahead / 0 behind** | 純 ff，可執行，但屬 main 寫入 |
| **O-1** r18 graft | 「298 commit 無共同祖先，需你簽」 | **不只是無共同祖先——兩個樹只有 230 個共同路徑** | **不是 merge，是樹的調和** |

---

## 1. D-H：降級

```
git log --all -- "Fine-grained personal access tokens.txt"   → 0 筆
grep -c "Fine-grained" .gitignore                            → 1
```

**該憑證從未進入版本歷史，且已被忽略。** 所以：

- **不需要**歷史改寫（history rewrite）
- **不需要**緊急輪替
- 仍建議輪替，但這是**衛生**，不是**事故**

我前幾輪把它寫成「需移出並輪替（D-H）」，讀起來像洩漏。**實際是從未進 repo。** 這一項從「待你處理」降級為「建議事項」。

---

## 2. O-2：乾淨，但仍是 main 寫入

```
merge/epoch-40-ff-20261101  →  4 ahead / 0 behind origin/main
```

純 fast-forward，零衝突、零 merge commit。指令：

```bash
git push origin merge/epoch-40-ff-20261101:main
# 回退：git push --force-with-lease origin <舊main sha>:main
```

**我沒有執行。** 理由不是能力，是 `AGENTS.md` 明文 "Do not push, merge"——這一條與「車道能不能跑」無關，是**授權邊界**。我可以把 ff 準備到一步之遙，但把 main 往前推需要你按下去。

---

## 3. O-1：真正的發現

我前幾輪說「298 commit、無共同祖先、graft 會改寫拓撲」。**那是真的，但它是次要問題。**

實測（`git ls-tree` 逐路徑比對）：

| | 檔案數 |
|---|---|
| `origin/main` 樹 | **746** |
| `candidate/r18` 樹 | **2,079** |
| **兩者共同路徑** | **230** |
| **只在 main** | **516** |
| **只在 r18** | **1,849** |

**只有 230 個路徑同時存在於兩邊。** 這不是兩條分岔的歷史，是**兩個不同的樹**。

### 3.1 main 上那 516 個檔案是什麼

| 目錄 | 檔案數 |
|---|---|
| `fhs_msc_handoff_20261030/` | **223** |
| `evidence/` | 142 |
| `tests/` | 73 |
| `b1_closure_20261028/` | 30 |
| `src/` | **27** |
| `tools/` / `scripts/` / `openspec/` | 16 |

**main 不是一條該被吸收的舊分支。** 它上面有一整套 223 檔的 `fhs_msc_handoff_20261030`（正是本次交付的相關樹）、142 個 evidence、73 個 tests、27 個 src 檔——**這些 r18 全都沒有**。

### 3.2 所以 graft 是錯的工具

`git merge --allow-unrelated-histories` 在 230 個共同路徑上會產生衝突，而另外 516 + 1,849 個路徑會原樣並存——**結果是一個 2,595 檔的混合樹，沒有人能判斷哪些是權威。**

正確做法是**內容級調和**，不是歷史嫁接：

1. **先分類 516 個 main-only 檔案**：`fhs_msc_handoff_20261030/`（223）與 `src/`（27）最可能與交付相關，優先判定
2. 需要的 → 以**單一 adoption commit** 複製到 r18（可逐檔 review）
3. 不需要的 → 留在 main，或標 `RETIRED`
4. **歷史保持分岔**——分岔的歷史不是問題，混合的樹才是

---

## 4. 裁決

| # | 裁決 | 依據 |
|---|---|---|
| **1** | **D-H 降級為衛生事項** | 從未 commit、已 ignore |
| **2** | **O-2 可執行，但屬 main 寫入，留給你按** | 4 ahead / 0 behind，`AGENTS.md` 禁 merge |
| **3** | **O-1 撤回「graft」提案** | 230 共同路徑 / 516 main-only / 1,849 r18-only = 兩個樹 |
| **4** | O-1 改為「內容級 adoption」：先分類 516 檔 | 混合樹無法判斷權威 |
| **5** | 不再把 O-1 描述成「需要你簽的危險操作」 | 它需要的是**分類工作**，不是簽章 |

---

## 5. 可執行方案

```bash
# 1. 匯出 main-only 清單，按目錄分類（已算出：516 檔，7 個頂層目錄）
git ls-tree -r --name-only origin/main > main.txt
git ls-tree -r --name-only HEAD       > r18.txt
comm -23 <(sort main.txt) <(sort r18.txt) > main_only.txt

# 2. 先判 fhs_msc_handoff_20261030/（223 檔）與 src/（27 檔）是否屬於本交付
#    —— 這兩組決定 O-1 是「併入」還是「保留分岔」

# 3. 需要的以單一 commit 併入 r18；不需要的標 RETIRED
# 4. main 與 r18 的歷史維持分岔
```

**第 2 步是唯一需要判斷的地方，而且它是技術判斷，不是授權判斷。**

---

## 6. 教訓

我把 O-1 掛在「需要你簽」上好幾輪。實際去量之後，它是**兩個樹**——一個我從來沒打開看的問題。

**「需要授權」和「需要工作」長得很像，而前者比較好說出口。** 這次量出來的 230 / 516 / 1,849 三個數字，把 O-1 從授權問題變回工程問題。
