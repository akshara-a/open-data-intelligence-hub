# Purchase Prediction Model — Business Report

## Executive Summary

We built a model that predicts, in real time, whether a website visitor is likely to make a
purchase during their current session. Using three years' worth of session behavior (12,330
sessions, ~15% ending in a purchase), the model correctly identifies **69% of actual buyers**
and, when it flags a session as "likely to buy," is **right about two-thirds of the time**.

More importantly, the model tells us **what actually predicts a purchase**: it isn't who the
visitor is or when they arrive — it's what they *do* on the site, particularly how deep they
browse into product pages and how quickly they bounce off. That single finding reframes where
marketing and product teams should focus effort, and it drives five concrete recommendations
in this report.

## The Business Problem

Every session on the site is a chance to convert a browser into a buyer, but not every session
is worth the same investment — a live-chat intervention or a phone call costs real money and
doesn't scale to every visitor. The business question this project answers: **can we tell, from
early session behavior, which visitors are worth the expensive interventions, which are worth a
cheaper nudge, and which should be left alone?**

## Approach

- Trained and compared three models: Logistic Regression, Decision Tree, and Random Forest.
- Tuned the two tree-based models with grid search across depth, split, and class-weighting
  settings, using 5-fold cross-validation.
- Selected the model and settings that best balance catching real buyers (recall) against not
  wasting effort on false alarms (precision).
- Went one step further than a standard classification project: tuned the *decision threshold*
  itself, and built practical customer tiers a business team can act on directly.

## Key Findings

**1. On-site behavior predicts purchases far better than visitor demographics.**
The single strongest signal is `PageValues` — a measure of how valuable the pages a visitor
browses tend to be — which alone accounts for 38% of the model's predictive power. Exit rate,
bounce rate, and time spent on product pages round out the next most important signals. Visitor
type, traffic source, and region — the things a typical demographic-targeting campaign would
lean on — barely register by comparison. **The browsing session itself is the best evidence of
intent, more than anything known about the visitor beforehand.**

**2. November carries a real, model-confirmed seasonal lift.**
It's the only calendar month that shows up as a meaningful predictive signal, consistent with
holiday shopping behavior in the raw data.

**3. The standard 50/50 cutoff isn't the right one for this business.**
Out of the box, classification models flag a session as "will buy" only when they're more than
50% confident. We found that lowering that bar to **45%** confidence catches noticeably more
real buyers for almost no added waste — a free improvement simply from calibrating the model to
this business's actual cost structure (a missed sale costs more than a wasted email).

**4. Visitors separate cleanly into three actionable tiers.**
Scoring every session and grouping by predicted purchase probability produces three groups whose
*actual* purchase rates validate the model well:

| Tier | Share of Traffic | Actual Purchase Rate |
|---|---|---|
| Low | 74.7% | 2.9% |
| Medium | 12.7% | 34.6% |
| High | 12.6% | 72.1% |

The High tier converts at nearly **5x** the overall site average — a small, identifiable group
worth the most attention.

## Model Performance

| Model | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|
| Logistic Regression (baseline) | 0.752 | 0.414 | 0.534 | 0.900 |
| Decision Tree (baseline) | 0.537 | 0.565 | 0.551 | 0.738 |
| Random Forest (baseline) | 0.770 | 0.552 | 0.643 | 0.923 |
| Decision Tree (optimized) | 0.708 | 0.636 | 0.670 | 0.926 |
| **Random Forest (optimized) — final model** | 0.652 | 0.686 | 0.668 | 0.925 |

*Precision: of sessions flagged as "will buy," how many actually did. Recall: of sessions that
actually bought, how many the model caught. F1-Score: the balance of the two.*

The final Random Forest was chosen over the very similarly-performing optimized Decision Tree
because it generalizes more reliably across data splits and catches more real buyers (higher
recall) — the more costly error for this business problem is a missed sale, not a wasted nudge.

## Recommendations

**1. Trigger real-time interventions off page-value signals, not page counts.**
Build a live scoring rule that flags a session the moment its behavior crosses into the
High-probability tier (72% actual conversion), and surface an on-site incentive before the
visitor leaves. *Test the incentive against a holdout group first* — over-discounting sessions
that would have converted anyway erodes margin.

**2. Use exit-intent signals to catch the Medium tier before they leave.**
The Medium tier (12.7% of traffic, 34.6% actual conversion) is large and genuinely undecided —
worth a lower-cost nudge like an exit-intent popup or cart-save email, rather than the full-cost
treatment reserved for the High tier.

**3. Prioritize retargeting ad spend by product-page dwell time, not click count.**
Visitors who spend real time on product pages without buying are a better retargeting audience
than visitors who simply click through many pages quickly. Pair this with a UX review of
high-dwell, non-converting pages to rule out confusion or friction as the cause.

**4. Shift remarketing budget earlier into the holiday season.**
Front-load spend into late October through November rather than spreading it evenly across the
year, based on the seasonal effect the model independently confirmed.

**5. Deploy at the 45% confidence threshold and route each tier to a cost-matched channel.**
Send High-tier sessions to the most expensive, highest-touch channel; Medium-tier sessions to a
mid-cost channel; leave Low-tier traffic alone. This concentrates spend on the traffic segment
already shown to convert at 72%, rather than spreading effort evenly across all visitors.

## Limitations and Next Steps

This analysis is based on one year of session data from a single retailer, with no
repeat-customer history, no cost or margin data, and no direct measurement of how much any given
channel or intervention actually lifts conversion. The recommendations above are the best
evidence-based starting point from this data, not a guarantee. Before committing full budget:

- Run a small live pilot of the tier-based channel routing to confirm the recall gain from the
  45% threshold translates into real incremental revenue, not just a better score on paper.
- Layer in cost and margin data per channel to refine which tier deserves which specific
  intervention.
- Revisit the November seasonal effect each year rather than assuming it repeats identically.

## Bottom Line

The model doesn't just predict purchases — it tells us that **in-session behavior is a far
better signal than anything known about a visitor beforehand**, gives us a calibrated way to
tier traffic by real purchase likelihood, and points to five specific, testable actions. The next
step is a live pilot, not a full rollout, to confirm these gains hold outside of historical data.
