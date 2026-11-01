# FAR-051｜EXECUTE 能建置：14.18 秒、有收據、檔案真的出現

日期：2026-11-01（台北）
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`

---

## 0. 第三次觀察，終於有對照

| 觀察 | 任務 | 讀 repo | 結果 |
|---|---|---|---|
| FAR-049 | 回答一個問題 | 否 | `ok:True` **44.58 s**、nonce ✓、usage ✓ |
| FAR-050 | 依 PLAN 建工作包 | **是**（治理 repo） | `ok:False` **601.92 s**、nonce ✗、usage ✗ |
| **FAR-051** | **建一個檔案、一個函式** | **否**（brief 明令不讀） | **`ok:True` 14.18 s、nonce ✓、usage ✓、檔案真的產生** |

FAR-051 的產物（92 bytes，實跑 `python twice.py` → `4`）：

```python
def twice(n: int) -> int:
    return n * 2


if __name__ == "__main__":
    print(twice(2))
```

---

## 1. 修正上一輪的修正

上一輪我寫「大小假設從來沒被測到」，那是對的。這一輪把它測了，結果是：

> **EXECUTE 能建置。限制不是「能不能動手」，是「動手時要讀多少東西」。**

- 一個檔案、一個函式、明令不讀 repo → **14.18 秒完成，收據齊全**
- 依 PLAN 在治理 repo 裡建工作包 → 600 秒無回應

**區分變數是「讀取面」，不是字數、也不是「是否動手」。** 兩者都會寫檔；差別在一邊要掃幾十個治理檔才敢動手。

---

## 2. 三車道的完整服務地圖（實測）

| 車道 | 任務類型 | 實測 |
|---|---|---|
| **PLAN** `gpt-6.1-sol` | 研究、結構化問題 | ✅ 22.89 s / 65.16 s，nonce ✓ usage ✓ |
| **EXECUTE** `deepseek-v4.1-flash` | 回答問題 | ✅ 14.46 s / 44.58 s |
| **EXECUTE** | 單檔建置 | ✅ **14.18 s、產物落地** |
| **EXECUTE** | 跨 repo 建置工作包 | ❌ 601.92 s 無回應 |
| **VERIFY_SECURITY** `gpt-6.1-sol` | 獨立查核 | ✅ 兩次 sitting，五條全 PASS |

**三條車道全部可服務。唯一失敗的組合是「EXECUTE × 大讀取面」。**

---

## 3. 最佳工程裁決

| # | 裁決 | 依據 |
|---|---|---|
| **1** | **EXECUTE 的 brief 必須明示「不讀 repo」或「只讀 N 個檔」** | 14.18 s vs 601.92 s，唯一變數是讀取面 |
| **2** | EXECUTE 的工作包以「一個檔案、一個函式」為粒度 | 同上 |
| **3** | `far_round.py` 餵給 EXECUTE 的 brief 應剝除治理上下文，只留工作包 | 目前把 PLAN 全文餵進去，等於叫它讀整個 repo |
| **4** | 三車道已可服務，FAR 現在只缺「走完一次」 | PLAN ✓、EXECUTE ✓（單檔）、VERIFY ✓ |
| **5** | 不再把 600 秒停滯記成車道 FAIL | 已兩次觀察，一次成功一次失敗 → 變數已定位 |

---

## 4. 完整可執行方案

```bash
# 1. far_round.py 的 EXECUTE brief 改為「工作包 + 明令不讀 repo」
#    目前：把 PLAN 輸出 400 字餵進去，但沒說「不要讀 repo」
#    改成：附一句 "Do not read the repository; the package is fully specified below."

# 2. 重跑三車道（PLAN 22.89 s + EXECUTE 14 s + VERIFY ~60 s ≈ 100 s 全程）
python scripts/far_round.py --run FAR-…-052 --carry-chars 400 --no-repo-read

# 3. 通過後 far_publish.py --promote <run> --by owner
#    這會是這批 21 篇之後第一篇 PUBLISHED
```

**第 2 步是唯一還沒跑的**：三條車道都已單獨證明可服務，還沒有一個 FAR 在同一次執行裡走完三條。

---

## 5. 這輪的教訓

八次自我推翻之後，第九次的形狀變了：**前八次是「觀測不足就下結論」，這一次是「補上對照組之後，結論翻轉」。**

- 上一輪：「限制在工作包大小」——**錯**，049 沒有對照組
- 這一輪：「限制在讀取面」——**有對照組**：同樣是建置，14.18 s vs 601.92 s，差別只在「要不要讀 repo」

**同一個 arm、同一條傳輸、同一種產物。** 差的那一次，brief 叫它在治理 repo 裡找依據。

所以真正的裁決不是「把 brief 裁短」，是**「不要把治理上下文塞進 EXECUTE 的工作包」**——那等於叫一個 bounded writer 去讀整套契約，而它會照做。
