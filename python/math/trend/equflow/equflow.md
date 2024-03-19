https://latex.codecogs.com/eqneditor/editor.php

--

1a.

\begin{align*}
&& x_i \text{ (observed)} &= [\ldots] \quad , \\
&& y_i \text{ (observed)} &= [\ldots] \\
\end{align*}

1b.

\begin{align*}
&& \text{Data Series } (x,y): \\
&& x_i \text{ (observed)} &= [\ldots] \quad , \\
&& y_i \text{ (observed)} &= [\ldots] \\
\end{align*}

1r.

n \text{ (count)}

1s.

\begin{align*}
& n = \sum\limits_{i=1}^{n} 1 \\
& \text{(count)}
\end{align*}

1t.

\begin{align*}
& df = n - k -1 \\
& \text{(degree of freedom)}
\end{align*}

--

2a.

\begin{align*}
& \sum\limits_{i=1}^{n} x_i \quad , \\
& \sum\limits_{i=1}^{n} y_i \quad \\
& \text{(sum)}
\end{align*}

2r.

\begin{align*}
& \bar{x} \text{ (mean)} \quad , \\
& \bar{y} \text{ (mean)}
\end{align*}

--

3a.

\begin{align*}
& TSS_x = \sum\limits_{i=1}^{n} (x_i - \bar{x})^2 \quad , \\
& \sum\limits_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})  \\
\end{align*}

3r.

\begin{align*}
& \hat{\beta}_1 = m \text{ (slope)} \quad , \\
& \hat{\beta}_0 = b \text{ (intercept)} \quad , \\
& \hat{y}_i  \text{ (predicted)} = m \cdot x_i + b \\
\end{align*}

3s.

\begin{align*}
&& \hat{\beta}_1 &= m \text{ (slope)}     &= \frac{\text{Cov}(x,y)}{s_x^2} & \quad , \\
&& \hat{\beta}_0 &= b \text{ (intercept)} &= \bar{y} - m \bar{x} \quad \\
\end{align*}

3t.

\hat{y}_i  \text{ (predicted)} = m \cdot x_i + b


--

4a.

\begin{align*}
&     \sum\limits_{i=1}^{n} (x_i - \bar{x})^2  \quad ,
\quad \sum\limits_{i=1}^{n} (y_i - \bar{y})^2  \quad , \\
&     \sum\limits_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y}) \\
& \text{(sum square)}
\end{align*}

4r.

\begin{align*}
& s_x^2 \text{ (variance)} \quad , \\
& s_y^2 \text{ (variance)} \quad , \\
& \text{Cov}(x,y) \text{ (covariance)} \\
\end{align*}

4s.

\begin{align*}
& s_x \text{ (standard deviation)} \quad , \\ 
& s_y \text{ (standard deviation)} \quad , \\
& r_{x,y} \text{ (pearson)} = \frac{\text{Cov}(x,y)}{s_x . s_y} \\
\end{align*}

4t.

\begin{align*}
& R^2 _\text{ (linear)}= r_{x,y}^2 \quad ,  \\
& R^2 _\text{ (adjusted)} = 1 - \frac{{(1 - R^2)(n - 1)}}{{n - k - 1}} \\
\end{align*}

--

5a.

\begin{align*}
& \epsilon_i \text{ (residual)} = y_i - \hat{y}_i \quad ,  \\
& SSR = \epsilon^2 = \sum (y_i - \hat{y}_i)^2 \quad ,  \\
\end{align*}

5r.

\begin{align*}
& MSE = \frac{SSR}{df} \quad ,  \\
& SE(\beta_1) = \sqrt{\frac{MSE}{TSS_x}} = \sqrt{\frac{MSE}{\sum (x_i - \bar{x})^2}}  \\
\end{align*}

--

6a.

t \text { value} = \frac{\hat{\beta}_1}{SE(\hat{\beta}_1)}

6b.

p \text { value}

