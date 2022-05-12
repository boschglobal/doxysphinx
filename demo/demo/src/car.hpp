// =====================================================================================
// C O P Y R I G H T
// -------------------------------------------------------------------------------------
//  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
//
//  Author(s):
//  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
// =====================================================================================
#ifndef DEMO__CAR__INCLUDED
#define DEMO__CAR__INCLUDED

/// @brief The namespace doxysphinx contains all demo code that we need for demonstration of doxysphinx.
///
/// @rst
/// .. note::
///    We can add rst right into the doxygen comment.
/// @endrst
///
namespace doxysphinx {

/// @brief we can also add sphinx needs here for example:
///
/// @rst
/// .. component:: Restructured Text Demo
///    :id: COMP_rst_demo
///    :status: done
///
///    The rst demo is one component of the overall doxysphinx demo application.
/// @endrst
namespace rst {

/// @brief A car.
///
/// @rst
/// .. warning::
///    This car is a top secret prototype.
///
/// @endrst
///
/// Here is a plot to show it's true power:
///
/// @rst
/// .. plot::
///
///   import matplotlib
///   import matplotlib.pyplot as plt
///   import numpy as np
///
///   # Data for plotting
///   t = np.arange(0.0, 2.0, 0.01)
///   s = 1 + np.sin(2 * np.pi * t)
///
///   fig, ax = plt.subplots()
///   ax.plot(t, s)
///
///   ax.set(xlabel='time (s)', ylabel='voltage (mV)',
///         title='About as simple as it gets, folks')
///   ax.grid()
///
///   plt.show()
/// @endrst
class Car : public TopSecretPrototype<StyleProps::ExtraordinaryAwesomeness, EngineProps::UltraFast>
{
    public:
        /// @brief Creates a new instance of the Car.
        ///
        /// @param engine - the engine to use for this Car.
        /// @param color - the color of this Car.
        ///
        /// @rst
        /// .. hint::
        ///    Rst text can also be included after the params.
        ///
        /// @endrst
        Car(Engine& engine, Color& color) {};

        /// enter for driver
        void enter(Driver& driver);

        // enter for person
        void enter(Person& person);

        /// leave for person or driver
        void leave(Person& person);

        /// accelerates the car
        ///
        /// @rst
        /// .. tip::
        ///   The following is an example of a table contains formulas using Math LateX
        ///
        /// .. list-table:: Table 1.1 - useless symbols but looking very mathematical
        ///    :widths: 75 25
        ///    :header-rows: 1
        ///
        ///    * - Heading Description
        ///      - Heading Formula
        ///    * - Distance of the dynamic border from ego coordinate system at latexmath:[t=0]
        ///      - :math:`d_{Border}`
        ///    * - Course of the dynamic border
        ///      - :math:`s_{Border}(t)`
        ///    * - Acceleration of the dynamic border associated with the target object
        ///      - :math:`a_{Border}(t)`
        ///    * - Longitudinal vehicle velocity
        ///      - :math:`v_{Ego}(t)`
        ///    * - Longitudinal vehicle acceleration
        ///      - :math:`a_{Ego}(t)`
        /// @endrst
        void accelerate(float target_speed_ms);

        /// brakes the car
        void brake(float brake_force_nm);
}; // Car

} // rst
} // doxysphinx

#endif
