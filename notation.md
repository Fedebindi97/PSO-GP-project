$$vel_{i,t} = w \ vel_{i,t-1} + c_1r_1(pbest_{i}-pos_{i,t-1}) + c_2r_2(gbest-pos_{i,t-1})$$

$$pos_{i,t} = pos_{i,t-1} + vel_{i,t}$$

$$\underset{w}{max} \ w^{T}\mu - \frac{g}{2}w^{T}\Sigma w \\ s.t. \ \underset{i}{\sum}w_i=1$$