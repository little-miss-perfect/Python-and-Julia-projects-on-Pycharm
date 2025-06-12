# f(R) Gravity in Static and Spherically Symmetric Spacetimes

A Python program for exploring and testing f(R) modified-gravity models. This program implements:

- **Benchmark Models**  
  – Hu-Sawicki   
  – α<sub>L_L_M</sub> (Miranda)   
  – λ<sub>L_L_M</sub> (Starobinsky)  
  – An empty scenario directory is left for the user as a template for a new proposed model (make a copy in the same directory as the template and edit the copy)
- **Numerical boundary value problem Solver**  
  – Adapts a custom shooting method via SciPy's solve_ivp  
- **Shooting Method & Bracket Refinement**  
  – Automatically finds an approximate initial value R<sub>0</sub> to satisfy de Sitter boundary conditions  
  – Adaptive interval search expansion for R<sub>0</sub>, with root-finding using Brent’s method  
- **Potential associated to an f(R) model**  
  – Computes V(R) and its derivatives  
  – Locates nontrivial local minima via robust root-finding  
- **Plots**  
  – potential and its derivative  
  – Ricci scalar satisfying the de Sitter boundary condition

---

## Program Flowchart

Below is the full Mermaid flowchart of the program:

```mermaid
flowchart TD
    A[Start] --> B["Load scenario"]
    B --> C["Instantiate DerivativeFunctions & PotentialDerivative"]
    C --> D["Find the global minimum of the potential"]
    D --> E["Plot the potential & its derivative"]
    D --> F["find a valid interval to search for r_0"]
    F --> G["refine r0"]

    subgraph refine r_0 routine
        direction TB
        G --> S1["Initialize endpoints 'a, b' <br/>current_r0 = None<br/>step = 0"]
        S1 --> S2["Compute residuals:<br/>f_low = _residual(a)<br/>f_high = _residual(b)"]
        S2 --> S3{"|f_low| < tol_residual?<br/>and |f_high| < tol_residual?"}
        S3 -- yes --> S4["Return midpoint or last r0"]
        S3 -- no  --> S5{"check for a sign change<br/>sign(f_low) ≠ sign(f_high)?"}
        S5 -- yes --> S6["current_r0 = solver.solve(a, b)"]
        S5 -- no  --> S7{"current_r0 exists?"}
        S7 -- yes --> S4
        S7 -- no  --> S8["Error: invalid bracket"]
        S6 --> S9["Shrink/Expand bracket:<br/>δ = 10^(-(step+2))*(b - a)<br/>a = max(current_r0 - δ, a*0.8)<br/>b = min(current_r0 + δ, b*1.2)"]
        S9 --> S10["step += 1"]
        S10 --> S2
    end

    S4 --> H["use solve_ivp with r0_refined"]
    H --> I["plot the refined solution <br/> satisfying the de sitter boundary condition"]
    I --> J[End]
```

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.