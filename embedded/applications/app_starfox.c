#include "ch.h" // ChibiOS
#include "hal.h" // ChibiOS HAL
#include "mc_interface.h" // Motor control functions
#include "hw.h" // Pin mapping on this hardware
#include "timeout.h" // To reset the timeout

// starfox thread
static THD_FUNCTION(starfox_thread, arg);
static THD_WORKING_AREA(starfox_thread_wa, 2048); // 2kb stack for this thread

void app_starfox_init(void) {
	// Set the UART TX pin as an input with pulldown
	palSetPadMode(HW_UART_TX_PORT, HW_UART_TX_PIN, PAL_MODE_INPUT_PULLDOWN);

	// Start the starfox thread
	chThdCreateStatic(starfox_thread_wa, sizeof(starfox_thread_wa),
		NORMALPRIO, starfox_thread, NULL);
}

static THD_FUNCTION(starfox_thread, arg) {
	(void)arg;

	chRegSetThreadName("APP_STARFOX");

	for(;;) {
		// Read the pot value and scale it to a number between 0 and 1 (see hw_46.h)
		float pot = (float)ADC_Value[ADC_IND_EXT];
		pot /= 4095.0;

		if (palReadPad(HW_UART_TX_PORT, HW_UART_TX_PIN)) {
			// If the button is pressed, run the motor with speed control
			// proportional to the POT position with a speed between 0 ERPM
			// and 10000 ERPM
			mc_interface_set_pid_speed(pot * 10000.0);
		} else {
			// If the button is not pressed, release the motor
			mc_interface_release_motor();
		}

		// Run this loop at 500Hz
		chThdSleepMilliseconds(2);

		// Reset the timeout
		timeout_reset();
	}
}
