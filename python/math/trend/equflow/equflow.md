https://latex.codecogs.com/eqneditor/editor.php

--

1a.

\begin{align*}
&& x_i \text{ (observed)} &= [\ldots] \quad , \\
&& y_i \text{ (observed)} &= [\ldots] \\
\end{align*}

1r.

n \text{ (count)}

1s.

\begin{align*}
& df = n - k -1 \\
& \text{(degree of freedom)}
\end{align*}

--

2a.

\begin{align*}
& \sum\limits_{i=1}^{n} x_i \quad , \\
& \sum\limits_{i=1}^{n} y_i \quad
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

--

4a.

\begin{align*}
&     \sum\limits_{i=1}^{n} (x_i - \bar{x})^2  \quad ,
\quad \sum\limits_{i=1}^{n} (x_i - \bar{x})^2  \quad , \\
&     \sum\limits_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y}) , \\
\end{align*}

4r.

\begin{align*}
& s_X^2 \text{ (variance)} \quad , \\
& s_Y^2 \text{ (variance)} \quad , \\
& \text{Cov}(X,Y) \text{ (covariance)} \\
\end{align*}

4s.

\begin{align*}
& s_X \text{ (standard deviation)} \quad , \\ 
& s_Y \text{ (standard deviation)} \quad , \\
& r_{X,Y} \text{ (pearson)} = \frac{\text{Cov}(X,Y)}{s_X . s_Y} \\
\end{align*}

4t.

\begin{align*}
& R^2 _\text{ (linear)}= r_{X,Y}^2 \quad ,  \\
& R^2 _\text{ (adjusted)} = 1 - \frac{{(1 - R^2)(n - 1)}}{{n - k - 1}} \\
\end{align*}

--

5a.

\begin{align*}
& \epsilon_i = y_i - \hat{y}_i \quad ,  \\
& SSR = \epsilon^2 = \sum (y_i - \hat{y}_i)^2 \quad ,  \\
\end{align*}

5r.

\begin{align*}
& MSE = \frac{SSR}{df} \quad ,  \\
& SE(\beta_1) = \sqrt{\frac{MSE}{TSS_x}} = \sqrt{\frac{MSE}{\sum (x_i - \bar{x})^2}} \quad ,  \\
& t \text { value} = \frac{\hat{\beta}_1}{SE(\hat{\beta}_1)} \\
\end{align*}

--

6a.

p \text { value}

