import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Data.Finset.Card

/-!
# Claim 4: exact fixed-point softmax focusing

This file reconstructs the numerical core of Lemma 3.1 for arbitrary finite
index types. It does not enumerate lengths, scores, values, or tie patterns.

The construction uses source precision `b`, mixed precision `b' = 4b`, and
temperature `τ = 2⁻³ᵇ`. For `b ≥ 2`, a non-maximal score separated by one
source grid step is scaled down by at least `2²ᵇ ≥ 4b+1`. The standard strict
bound `1+x < exp x` then forces its exponential below half of one mixed-
precision grid step, so nearest rounding sends it exactly to zero. Maximal
scores have exponential one. Thus rounded SMAT and AHAT have identical
unnormalized weights, denominators, numerators, and outputs, including ties.
-/

noncomputable section

open Finset

namespace Claim4Exact

def gridStep (bits : ℕ) : ℝ := 1 / (2 : ℝ) ^ bits

def mixedBits (bits : ℕ) : ℕ := 4 * bits

def inverseTemperature (bits : ℕ) : ℝ := (2 : ℝ) ^ (3 * bits)

/-- Only the behavior at zero-underflow and exactly one matters below.
    This is the restriction of nearest-grid rounding to those two cases. -/
def relevantRound (step x : ℝ) : ℝ := if x < step / 2 then 0 else x

def roundedKernel (bits : ℕ) (maximum : ℝ) (score : ℝ) : ℝ :=
  relevantRound (gridStep (mixedBits bits))
    (Real.exp (inverseTemperature bits * (score - maximum)))

def hardKernel (maximum : ℝ) (score : ℝ) : ℝ :=
  if score = maximum then 1 else 0

theorem gridStep_pos (bits : ℕ) : 0 < gridStep bits := by
  unfold gridStep
  positivity

theorem gridStep_le_one (bits : ℕ) : gridStep bits ≤ 1 := by
  unfold gridStep
  positivity

theorem four_mul_add_one_le_four_pow :
    ∀ bits : ℕ, 2 ≤ bits → 4 * bits + 1 ≤ 4 ^ bits := by
  intro bits hbits
  induction bits, hbits using Nat.le_induction with
  | base => norm_num
  | succ n hn ih =>
      calc
        4 * (n + 1) + 1 = 4 * n + 5 := by omega
        _ ≤ 4 * (4 * n + 1) := by omega
        _ ≤ 4 * 4 ^ n := Nat.mul_le_mul_left 4 ih
        _ = 4 ^ (n + 1) := by rw [pow_succ]; ring

theorem four_mul_add_one_le_two_pow_two_mul
    (bits : ℕ) (hbits : 2 ≤ bits) :
    4 * bits + 1 ≤ 2 ^ (2 * bits) := by
  calc
    4 * bits + 1 ≤ 4 ^ bits := four_mul_add_one_le_four_pow bits hbits
    _ = 2 ^ (2 * bits) := by
      rw [show (4 : ℕ) = 2 ^ 2 by norm_num, ← pow_mul]

/-- A standard analytic certificate: `exp (-(n+1))` is strictly below the
    half-grid threshold at `n` fractional bits. -/
theorem exp_neg_succ_lt_half_grid (bits : ℕ) :
    Real.exp (-(bits + 1 : ℝ)) < gridStep bits / 2 := by
  have hexp : (2 : ℝ) < Real.exp 1 := by
    simpa using Real.add_one_lt_exp (by norm_num : (1 : ℝ) ≠ 0)
  have hp :
      (2 : ℝ) ^ (bits + 1) < Real.exp (bits + 1 : ℝ) := by
    calc
      (2 : ℝ) ^ (bits + 1) < (Real.exp 1) ^ (bits + 1) :=
        pow_lt_pow_left₀ hexp (by norm_num) (by omega)
      _ = Real.exp (bits + 1 : ℝ) := by
        rw [← Real.exp_nat_mul]
        norm_num
  have hinv :
      (Real.exp (bits + 1 : ℝ))⁻¹ <
        ((2 : ℝ) ^ (bits + 1))⁻¹ :=
    (inv_lt_inv₀ (Real.exp_pos _) (by positivity)).2 hp
  calc
    Real.exp (-(bits + 1 : ℝ)) =
        (Real.exp (bits + 1 : ℝ))⁻¹ := by rw [Real.exp_neg]
    _ < ((2 : ℝ) ^ (bits + 1))⁻¹ := hinv
    _ = gridStep bits / 2 := by
      simp [gridStep, pow_succ, div_eq_mul_inv]
      ring

theorem scaled_gap_at_least_mixed_bits_succ
    (bits : ℕ) (hbits : 2 ≤ bits) :
    (mixedBits bits : ℝ) + 1 ≤
      inverseTemperature bits * gridStep bits := by
  rw [show inverseTemperature bits * gridStep bits =
      (2 : ℝ) ^ (2 * bits) by
    unfold inverseTemperature gridStep
    rw [show 3 * bits = 2 * bits + bits by omega, pow_add]
    field_simp]
  exact_mod_cast four_mul_add_one_le_two_pow_two_mul bits hbits

theorem off_max_exponential_underflows
    (bits : ℕ) (hbits : 2 ≤ bits)
    (score maximum : ℝ)
    (hgap : score ≤ maximum - gridStep bits) :
    Real.exp (inverseTemperature bits * (score - maximum)) <
      gridStep (mixedBits bits) / 2 := by
  have hscale : 0 ≤ inverseTemperature bits := by
    unfold inverseTemperature
    positivity
  have harg :
      inverseTemperature bits * (score - maximum) ≤
        -((mixedBits bits : ℕ) + 1 : ℝ) := by
    have hdiff : score - maximum ≤ -gridStep bits := by linarith
    calc
      inverseTemperature bits * (score - maximum) ≤
          inverseTemperature bits * (-gridStep bits) :=
        mul_le_mul_of_nonneg_left hdiff hscale
      _ ≤ -((mixedBits bits : ℕ) + 1 : ℝ) := by
        have hs := scaled_gap_at_least_mixed_bits_succ bits hbits
        linarith
  calc
    Real.exp (inverseTemperature bits * (score - maximum)) ≤
        Real.exp (-((mixedBits bits : ℕ) + 1 : ℝ)) :=
      Real.exp_le_exp.mpr harg
    _ < gridStep (mixedBits bits) / 2 :=
      exp_neg_succ_lt_half_grid (mixedBits bits)

/-- Pointwise exact equivalence between the rounded softmax kernel and hard
    max-attention. The gap condition is exactly the one-grid-step consequence
    of distinct `b`-precision scores. -/
theorem roundedKernel_eq_hardKernel
    (bits : ℕ) (hbits : 2 ≤ bits)
    (maximum score : ℝ)
    (hle : score ≤ maximum)
    (hgridGap : score = maximum ∨
      score ≤ maximum - gridStep bits) :
    roundedKernel bits maximum score = hardKernel maximum score := by
  by_cases heq : score = maximum
  · subst score
    have hnot :
        ¬(1 : ℝ) < gridStep (mixedBits bits) / 2 := by
      have hstep := gridStep_le_one (mixedBits bits)
      linarith
    simp [roundedKernel, hardKernel, relevantRound, hnot]
  · have hgap : score ≤ maximum - gridStep bits :=
      hgridGap.resolve_left heq
    have hunder :=
      off_max_exponential_underflows bits hbits score maximum hgap
    simp [roundedKernel, hardKernel, relevantRound, heq, hunder]

theorem rounded_denominator_eq_hard
    {ι : Type*} (indices : Finset ι)
    (bits : ℕ) (hbits : 2 ≤ bits)
    (maximum : ℝ) (score : ι → ℝ)
    (hle : ∀ i ∈ indices, score i ≤ maximum)
    (hgridGap : ∀ i ∈ indices, score i = maximum ∨
      score i ≤ maximum - gridStep bits) :
    ∑ i ∈ indices, roundedKernel bits maximum (score i) =
      ∑ i ∈ indices, hardKernel maximum (score i) := by
  apply sum_congr rfl
  intro i hi
  apply roundedKernel_eq_hardKernel bits hbits maximum (score i)
  · exact hle i hi
  · exact hgridGap i hi

theorem rounded_numerator_eq_hard
    {ι : Type*} (indices : Finset ι)
    (bits : ℕ) (hbits : 2 ≤ bits)
    (maximum : ℝ) (score value : ι → ℝ)
    (hle : ∀ i ∈ indices, score i ≤ maximum)
    (hgridGap : ∀ i ∈ indices, score i = maximum ∨
      score i ≤ maximum - gridStep bits) :
    ∑ i ∈ indices, roundedKernel bits maximum (score i) * value i =
      ∑ i ∈ indices, hardKernel maximum (score i) * value i := by
  apply sum_congr rfl
  intro i hi
  rw [roundedKernel_eq_hardKernel bits hbits maximum (score i)
    (hle i hi) (hgridGap i hi)]

theorem rounded_attention_eq_hard
    {ι : Type*} (indices : Finset ι)
    (bits : ℕ) (hbits : 2 ≤ bits)
    (maximum : ℝ) (score value : ι → ℝ)
    (hle : ∀ i ∈ indices, score i ≤ maximum)
    (hgridGap : ∀ i ∈ indices, score i = maximum ∨
      score i ≤ maximum - gridStep bits) :
    (∑ i ∈ indices, roundedKernel bits maximum (score i) * value i) /
        (∑ i ∈ indices, roundedKernel bits maximum (score i)) =
      (∑ i ∈ indices, hardKernel maximum (score i) * value i) /
        (∑ i ∈ indices, hardKernel maximum (score i)) := by
  rw [rounded_numerator_eq_hard indices bits hbits maximum score value hle hgridGap]
  rw [rounded_denominator_eq_hard indices bits hbits maximum score hle hgridGap]

#print axioms exp_neg_succ_lt_half_grid
#print axioms off_max_exponential_underflows
#print axioms roundedKernel_eq_hardKernel
#print axioms rounded_attention_eq_hard

end Claim4Exact
