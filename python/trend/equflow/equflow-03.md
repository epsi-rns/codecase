\begin{align*}
&& \hat{y}_i &= \text{Model}(x_i) \\
\end{align*}


\begin{align*}
&& \hat{y}_i \text{ (predicted)} &= [\ldots] \\
\end{align*}

\begin{align*}
& \boldsymbol{\hat{\beta}} = (X^\top X)^{-1} X^\top \mathbf{y} \\
& \text{(use matrix operations to find coefficients)}
\end{align*}


\begin{aligned}
              &&    X \mathbf{\beta} &= \mathbf{y} \\
  \Rightarrow &&    X^\top X \mathbf{\beta} &= X^\top \mathbf{y} \\
  \Rightarrow &&    \mathbf{\beta} &= (X^\top X)^{-1} X^\top \mathbf{X}
\end{aligned}


\begin{align*}
\text{1st} && y &= \beta_0 + \beta_1 x \\
\text{2nd} && y &= \beta_0 + \beta_1 x + \beta_2 x^2 \\
\text{3rd} && y &= \beta_0 + \beta_1 x + \beta_2 x^2 + \beta_3 x^3 \\
& && \text{(polynomial degree)}
\end{align*}

\begin{array}{|c|c|c|}
\hline
    \textbf{Linear} & \textbf{Quadratic} & \textbf{Cubic} \\
\hline

\hline
    \mathbf{X}
    =
    \begin{bmatrix}
        1 & x_1 \\
        1 & x_2 \\
        \vdots & \vdots \\
        1 & x_n \\
    \end{bmatrix}, \,
    \mathbf{y}
    =
    \begin{bmatrix}
        y_1 \\
        y_2 \\
        \vdots \\
        y_n \\
    \end{bmatrix} &

    \mathbf{X}
    =
    \begin{bmatrix}
        1 & x_1 & x_1^2 \\
        1 & x_2 & x_2^2 \\
        \vdots & \vdots & \vdots \\
        1 & x_n & x_n^2 \\
    \end{bmatrix}, \,
    \mathbf{y}
    =
    \begin{bmatrix}
        y_1 \\
        y_2 \\
        \vdots \\
        y_n \\
    \end{bmatrix} &

    \mathbf{X}
    =
    \begin{bmatrix}
        1 & x_1 & x_1^2 & x_1^3 \\
        1 & x_2 & x_2^2 & x_2^3 \\
        \vdots & \vdots & \vdots & \vdots \\
        1 & x_n & x_n^2 & x_n^3 \\
    \end{bmatrix}, \,
    \mathbf{y}
    =
    \begin{bmatrix}
        y_1 \\
        y_2 \\
        \vdots \\
        y_n \\
    \end{bmatrix} \\
\hline

\hline
    \left(\mathbf{X}^T \mathbf{X}\right)
    \begin{bmatrix}
        \beta_0 \\ \beta_1 \\
    \end{bmatrix} 
    = \mathbf{X}^T \mathbf{y} &

    \left(\mathbf{X}^T \mathbf{X}\right)
    \begin{bmatrix}
        \beta_0 \\ \beta_1 \\ \beta_2 \\
    \end{bmatrix} 
    = \mathbf{X}^T \mathbf{y} &

    \left(\mathbf{X}^T \mathbf{X}\right)
    \begin{bmatrix}
        \beta_0 \\ \beta_1 \\ \beta_2 \\ \beta_3 \\
    \end{bmatrix} 
    = \mathbf{X}^T \mathbf{y} \\
\hline

\end{array}


