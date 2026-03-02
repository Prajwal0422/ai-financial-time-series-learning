# Day 2 – Returns and Volatility (The Math of Stock Data)

Yesterday, we learned that a stock is just a **time-series signal** (OHLC data). Today, we move from just looking at prices to understanding **how prices change**.

In Data Science, we don't just care about the price being $100 or $110. We care about the **percentage change** between them. This is called a **Return**.

---

## 1. Simple Returns
A simple return is the percentage change in price from one day to the next.

**Formula:**
$$Simple Return = \frac{Price_{Today} - Price_{Yesterday}}{Price_{Yesterday}}$$

**Example:**
- Yesterday Price: $100
- Today Price: $105
- Return = $(105 - 100) / 100 = 0.05$ or **5%**

**Why use returns instead of price?**
- Returns are **normalized**. A $5 move on a $10 stock is HUGE (50%), but a $5 move on a $1000 stock is TINY (0.5%).
- Returns allow us to compare different stocks easily.

---

## 2. Log Returns (The "Pro" Way)
In quantitative finance and ML, we often use **Log Returns**.

**Formula:**
$$Log Return = \ln\left(\frac{Price_{Today}}{Price_{Yesterday}}\right)$$

**Why use Log Returns?**
1. **Additivity:** If you have returns for Day 1, Day 2, and Day 3, you can just *add* them to get the total return. (With simple returns, you have to multiply).
2. **Normal Distribution:** Log returns often follow a "Normal Distribution" (Bell Curve) more closely than simple returns, which makes ML models work better.

---

## 3. Volatility (Risk / Noise)
Volatility is a measure of how much the price "jumps around." 

In Data Science terms, Volatility is simply the **Standard Deviation** of returns.

- **Low Volatility:** The price moves in small, predictable steps.
- **High Volatility:** The price swings wildly up and down.

**DS Skill Alert:** We use a **Rolling Window** to calculate volatility. For example, "What was the volatility over the last 20 days?"

---

## 4. Why this matters for AI?
1. **Feature Engineering:** We will use Returns and Volatility as *inputs* (features) for our AI models.
2. **Regime Detection:** High volatility often means a "stressed" market, while low volatility means a "stable" market. Our AI needs to know the difference!

---

## 🧠 Homework for Today
1. Look at the `analysis/returns.py` file in your project.
2. Can you see where `pct_change()` (Simple Return) and `np.log()` (Log Return) are used?
3. Don't worry about the code yet, just try to match the math we learned today to the code lines.

---

## 🗓 Tomorrow (Day 3 Preview)
We will look at **Technical Indicators** (MA, RSI) and how they turn raw data into "signals" for our pattern recognition system.
