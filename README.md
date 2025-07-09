## Interactive Vector Field Simulation
This project is an interactive computational tool designed to help users visualize, manipulate, and analyze two-dimensional vector fields. At its core, it combines mathematical concepts from vector calculus with intuitive graphical interaction, making abstract field properties accessible and visually engaging.

A vector field in two dimensions assigns a vector (with both magnitude and direction) to every point in a plane. Mathematically, such a field is often written as:

![image](https://github.com/user-attachments/assets/a2c5ae37-2e8c-402c-8975-5bb834b8a9b3)

 
where U(x,y) and V(x,y) are the field's components in the x and y directions, respectively.

# Initial Field Construction
The project begins by letting the user define a uniform vector field. This means every point in the grid has the same vector, determined by user-supplied constants a and b. A key feature is the ability to draw arrows directly onto the field. Each arrow is mathematically interpreted as a localized perturbation—an influence that modifies the field in its vicinity. When a user draws an arrow from 
(x0,y0) to (x1,y1), it represents a vector influence with direction and strength proportional to the arrow's length and orientation.

The effect of each arrow is not limited to a single point; instead, it decays with distance from its origin, affecting the entire field but most strongly near where it was drawn. This is modeled as:

![image](https://github.com/user-attachments/assets/3452abc9-d2ea-4f73-b327-44050df53516)
 
The resultant field is the sum of the initial uniform field and the cumulative effects of all user-drawn arrows:

# Field Analysis: Gradient, Divergence, and Curl
The tool offers further insight by enabling overlays of key vector calculus properties:
- Gradient Magnitude: Measures how rapidly the field changes in space. It is computed as the root of the sum of squares of all spatial derivatives of the field components.
- Divergence: Indicates the presence of sources (where field lines spread out) or sinks (where they converge)
- Curl: Measures the tendency of the field to induce rotation around a point:
 
These properties are computed numerically using finite differences and visualized as color overlays, making abstract mathematical concepts tangible.

Example:
![image](https://github.com/user-attachments/assets/8b98bd29-13e3-411b-9b56-704f9a7d9906)



This could serve as an educational bridge between theory and intuition. It enables users to experiment with field configurations, observe the effects of local changes, and develop a deeper understanding of core vector calculus concepts such as divergence and curl—all within an accessible graphical environment.
