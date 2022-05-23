// =====================================================================================
// C O P Y R I G H T
// -------------------------------------------------------------------------------------
//  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
//
//  Author(s):
//  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
// =====================================================================================
#ifndef DEMO__ENGINE_INCLUDED
#define DEMO__ENGINE_INCLUDED

namespace doxysphinx {

namespace rst {

/// @brief An engine
///
/// @rst
/// .. danger::
///    This engine is even more top secret than the :demo:`doxysphinx::rst::Car`
///
/// @endrst
///
class Engine : public TopSecretPrototype<MaterialProps::HighDurablePlastics, PowerProps::Nm5000>
{
    public:
        /// @brief Creates a new instance of the Engine.
        ///
        /// This is a constructor.
        Engine() {};

        /// turns the engine off
        void turn_on();


        /// turns the engine on
        void turn_off();

        /// gets the current u/min.
        float current_umin();

}; // Engine

} // rst
} // doxysphinx

#endif
