"""
Power monitoring utility for LM2596S buck converter and L298N motor driver.
This script helps monitor power consumption and voltage levels during operation.
"""

import time
import RPi.GPIO as GPIO
from config import *

class PowerMonitor:
    def __init__(self):
        """Initialize power monitoring system."""
        self.monitoring = False
        print("Power Monitor initialized")
        print("Note: This is a software monitor. Use multimeter for accurate voltage readings.")
    
    def calculate_power_consumption(self, voltage, current):
        """Calculate power consumption."""
        return voltage * current
    
    def estimate_motor_current(self, pwm_duty_cycle):
        """Estimate motor current based on PWM duty cycle."""
        # Rough estimation: 0.5A at 50% PWM, 2.8A at 100% PWM
        base_current = 0.1  # Base current when stopped
        max_current = 2.8   # Maximum stall current
        estimated_current = base_current + (max_current - base_current) * (pwm_duty_cycle / 100)
        return estimated_current
    
    def display_power_info(self):
        """Display power system information."""
        print("\n=== Power System Information ===")
        print(f"Battery Voltage: {BATTERY_VOLTAGE}V (input to LM2596S)")
        print(f"Motor Voltage: {MOTOR_VOLTAGE}V (output from LM2596S)")
        print(f"Pi Voltage: {PI_VOLTAGE}V (for Raspberry Pi)")
        print()
        print("LM2596S Specifications:")
        print(f"  Input Range: {LM2596S_INPUT_VOLTAGE_MIN}-{LM2596S_INPUT_VOLTAGE_MAX}V")
        print(f"  Output Range: {LM2596S_OUTPUT_VOLTAGE_MIN}-{LM2596S_OUTPUT_VOLTAGE_MAX}V")
        print(f"  Max Current: {LM2596S_MAX_CURRENT}A")
        print(f"  Recommended Current: {LM2596S_RECOMMENDED_CURRENT}A")
        print()
        print("L298N Specifications:")
        print(f"  Voltage Drop: {L298N_VOLTAGE_DROP}V")
        print(f"  Max Current per Channel: {L298N_MAX_CURRENT}A")
        print()
        print("Expected Voltage Chain:")
        print(f"  {BATTERY_VOLTAGE}V (Battery) → {MOTOR_VOLTAGE}V (LM2596S) → {MOTOR_VOLTAGE - L298N_VOLTAGE_DROP}V (Motors)")
    
    def monitor_motor_operation(self, pwm_duty_cycle, duration=5):
        """Monitor power during motor operation."""
        print(f"\n=== Monitoring Motor Operation ===")
        print(f"PWM Duty Cycle: {pwm_duty_cycle}%")
        print(f"Duration: {duration} seconds")
        
        # Estimate current draw
        estimated_current = self.estimate_motor_current(pwm_duty_cycle)
        total_current = estimated_current * 2  # Two motors
        
        print(f"Estimated Current per Motor: {estimated_current:.2f}A")
        print(f"Total Estimated Current: {total_current:.2f}A")
        
        # Check if within limits
        if total_current > LM2596S_RECOMMENDED_CURRENT:
            print("⚠️  WARNING: Current exceeds recommended limit!")
            print("   Consider reducing PWM duty cycle or adding heat sink")
        
        # Calculate power consumption
        motor_power = self.calculate_power_consumption(MOTOR_VOLTAGE, total_current)
        print(f"Estimated Motor Power: {motor_power:.2f}W")
        
        # Estimate battery life
        if total_current > 0:
            battery_capacity_ah = 2.3  # Typical 12V battery capacity
            estimated_runtime = battery_capacity_ah / total_current
            print(f"Estimated Runtime: {estimated_runtime:.1f} hours")
        
        print("\nMonitoring... (Use multimeter to verify actual values)")
        time.sleep(duration)
        print("Monitoring complete")
    
    def power_system_test(self):
        """Run comprehensive power system test."""
        print("\n=== Power System Test ===")
        
        # Display system info
        self.display_power_info()
        
        # Test different PWM levels
        test_levels = [25, 35, 50, 70, 100]
        
        for pwm in test_levels:
            print(f"\n--- Testing {pwm}% PWM ---")
            self.monitor_motor_operation(pwm, 2)
            time.sleep(1)
        
        print("\n=== Power System Test Complete ===")
        print("Recommendations:")
        print("1. Use multimeter to verify actual voltage levels")
        print("2. Monitor temperature of LM2596S during operation")
        print("3. Keep current under 2A for optimal performance")
        print("4. Add heat sink if operating at high power")
    
    def battery_life_estimator(self, pwm_duty_cycle, battery_capacity_ah=2.3):
        """Estimate battery life for given PWM duty cycle."""
        estimated_current = self.estimate_motor_current(pwm_duty_cycle)
        total_current = estimated_current * 2  # Two motors
        pi_current = 0.5  # Pi Zero 2W current
        
        total_system_current = total_current + pi_current
        
        if total_system_current > 0:
            runtime_hours = battery_capacity_ah / total_system_current
            runtime_minutes = runtime_hours * 60
            
            print(f"\n=== Battery Life Estimation ===")
            print(f"PWM Duty Cycle: {pwm_duty_cycle}%")
            print(f"Battery Capacity: {battery_capacity_ah}Ah")
            print(f"Estimated Motor Current: {total_current:.2f}A")
            print(f"Pi Current: {pi_current}A")
            print(f"Total System Current: {total_system_current:.2f}A")
            print(f"Estimated Runtime: {runtime_hours:.1f} hours ({runtime_minutes:.0f} minutes)")
            
            return runtime_hours
        else:
            print("Invalid current calculation")
            return 0
    
    def thermal_management_check(self, pwm_duty_cycle):
        """Check if thermal management is needed."""
        estimated_current = self.estimate_motor_current(pwm_duty_cycle)
        total_current = estimated_current * 2
        
        print(f"\n=== Thermal Management Check ===")
        print(f"PWM Duty Cycle: {pwm_duty_cycle}%")
        print(f"Estimated Current: {total_current:.2f}A")
        
        if total_current > LM2596S_RECOMMENDED_CURRENT:
            print("🔴 HEAT SINK REQUIRED")
            print("   - Current exceeds 2A recommended limit")
            print("   - LM2596S will generate significant heat")
            print("   - Install heat sink immediately")
        elif total_current > 1.5:
            print("🟡 HEAT SINK RECOMMENDED")
            print("   - Current approaching 2A limit")
            print("   - Consider adding heat sink for extended operation")
        else:
            print("🟢 NO HEAT SINK NEEDED")
            print("   - Current within safe operating range")
            print("   - LM2596S should operate cool")
    
    def interactive_monitor(self):
        """Interactive power monitoring mode."""
        print("\n=== Interactive Power Monitor ===")
        print("Commands:")
        print("info - Display power system information")
        print("test - Run power system test")
        print("monitor <pwm%> - Monitor specific PWM level")
        print("battery <pwm%> - Estimate battery life")
        print("thermal <pwm%> - Check thermal management needs")
        print("quit - Exit monitor")
        
        while True:
            try:
                command = input("\nEnter command: ").lower().strip()
                
                if command == 'quit':
                    break
                elif command == 'info':
                    self.display_power_info()
                elif command == 'test':
                    self.power_system_test()
                elif command.startswith('monitor '):
                    try:
                        pwm = int(command.split()[1])
                        if 0 <= pwm <= 100:
                            self.monitor_motor_operation(pwm)
                        else:
                            print("PWM must be between 0 and 100")
                    except (ValueError, IndexError):
                        print("Usage: monitor <pwm%>")
                elif command.startswith('battery '):
                    try:
                        pwm = int(command.split()[1])
                        if 0 <= pwm <= 100:
                            self.battery_life_estimator(pwm)
                        else:
                            print("PWM must be between 0 and 100")
                    except (ValueError, IndexError):
                        print("Usage: battery <pwm%>")
                elif command.startswith('thermal '):
                    try:
                        pwm = int(command.split()[1])
                        if 0 <= pwm <= 100:
                            self.thermal_management_check(pwm)
                        else:
                            print("PWM must be between 0 and 100")
                    except (ValueError, IndexError):
                        print("Usage: thermal <pwm%>")
                else:
                    print("Unknown command")
            
            except KeyboardInterrupt:
                print("\nExiting monitor...")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    """Main function for power monitoring."""
    print("=== LM2596S Power Monitor ===")
    print("This tool helps monitor and optimize your power system.")
    
    monitor = PowerMonitor()
    
    try:
        monitor.interactive_monitor()
    except KeyboardInterrupt:
        print("\nPower monitor stopped")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
