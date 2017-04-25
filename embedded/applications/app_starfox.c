#include "ch.h" // ChibiOS
#include "hal.h" // ChibiOS HAL
#include "mc_interface.h" // Motor control functions
#include "hw.h" // Pin mapping on this hardware
#include "timeout.h" // To reset the timeout

// starfox thread
static THD_FUNCTION(starfox_thread, arg);
static THD_WORKING_AREA(starfox_thread_wa, 2048); // 2kb stack for this thread
bool pressed = false;

void app_starfox_init(void) {
	// Set the UART TX and RX pins as an input with pullup
	//palSetPadMode(HW_UART_TX_PORT, HW_UART_TX_PIN, PAL_MODE_INPUT_PULLUP);
	//palSetPadMode(HW_UART_RX_PORT, HW_UART_RX_PIN, PAL_MODE_INPUT_PULLUP);

	palSetPadMode(HW_UART_TX_PORT, HW_UART_TX_PIN, PAL_MODE_INPUT | PAL_STM32_PUDR_PULLUP);
	palSetPadMode(HW_UART_RX_PORT, HW_UART_RX_PIN, PAL_MODE_INPUT | PAL_STM32_PUDR_PULLUP);
	palSetPadMode(HW_ICU_GPIO, HW_ICU_PIN, PAL_MODE_OUTPUT_PUSHPULL);

	// Start the starfox thread
	chThdCreateStatic(starfox_thread_wa, sizeof(starfox_thread_wa),
		NORMALPRIO, starfox_thread, NULL);
}

void app_starfox_release(void) {
	pressed = true;
	palSetPad(HW_ICU_GPIO, HW_ICU_PIN);
	chThdSleepMilliseconds(200);
	palClearPad(HW_ICU_GPIO, HW_ICU_PIN);
	chThdSleepMilliseconds(500);
	pressed = false;

}

static THD_FUNCTION(starfox_thread, arg) {
	(void)arg;

    float pot;
	bool manual_set = false;
	
	palClearPad(HW_ICU_GPIO, HW_ICU_PIN);

	chRegSetThreadName("APP_STARFOX");

	for(;;) {

		if (!palReadPad(HW_UART_RX_PORT, HW_UART_RX_PIN)){
			manual_set = true;
            if (!palReadPad(HW_UART_TX_PORT, HW_UART_TX_PIN)) {

				if(!pressed) app_starfox_release();

            }

            pot = (float)ADC_Value[ADC_IND_EXT];
            pot /= 4095.0;
            mc_interface_set_pid_speed(pot * 30000.0);

        }

        else {
				if(manual_set) {
					//mc_interface_set_pid_speed(0);
					mc_interface_release_motor();
					manual_set = false;
				}
				pot = 0;
				// If the button is not pressed, release the motor
    			//mc_interface_release_motor();
                // Hold Batch
    	}


		// Run this loop at 500Hz
		chThdSleepMilliseconds(2);

		// Reset the timeout
		timeout_reset();
	}
}
