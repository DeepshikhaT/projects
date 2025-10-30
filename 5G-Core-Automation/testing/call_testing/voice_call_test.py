#!/usr/bin/env python3
"""
Voice Call Testing Script
==========================
This script simulates and tests voice calls in 5G network

What it does:
1. Simulates two 5G phones (UE1 and UE2)
2. Registers both phones to the network
3. Makes UE1 call UE2
4. Monitors call quality (MOS, latency, jitter)
5. Generates test report

Author: Deepshikha Tripathi
"""

import time
import argparse
from datetime import datetime

class UESimulator:
    """
    Simulates a 5G User Equipment (phone)

    In real life, this would be actual 5G phone/modem
    For demo purposes, we simulate the phone behavior
    """

    def __init__(self, imsi, msisdn=None):
        """
        Initialize UE simulator

        Args:
            imsi: International Mobile Subscriber Identity (like phone's ID)
                  Example: "001010000000001"
            msisdn: Phone number (like +1-555-1234)
        """
        self.imsi = imsi
        self.msisdn = msisdn or f"+1555{imsi[-7:]}"
        self.registered = False
        self.ip_address = None
        self.call_active = False

        print(f"[INFO] Created UE: IMSI={self.imsi}, Phone={self.msisdn}")

    def register(self):
        """
        Register phone to 5G network

        Real Process:
        1. Phone sends: Registration Request
        2. AMF responds: Authentication Request
        3. Phone sends: Authentication Response
        4. AMF responds: Security Mode Command
        5. Phone sends: Security Mode Complete
        6. AMF responds: Registration Accept

        We simulate this process
        """
        print(f"\n[STEP] Registering {self.imsi} to network...")

        # Simulate registration steps
        steps = [
            "Sending Registration Request",
            "Performing Authentication",
            "Completing Security Setup",
            "Receiving Registration Accept"
        ]

        for i, step in enumerate(steps, 1):
            time.sleep(0.5)  # Simulate network delay
            print(f"  [{i}/4] {step}...")

        self.registered = True
        print(f"[✓] {self.imsi} successfully registered!")
        return True

    def establish_pdu_session(self, dnn="internet"):
        """
        Establish data session (PDU Session)

        Real Process:
        1. Phone sends: PDU Session Establishment Request
        2. SMF allocates IP address
        3. SMF configures UPF to route traffic
        4. SMF responds: PDU Session Establishment Accept

        Args:
            dnn: Data Network Name (like "internet" or "ims")
        """
        if not self.registered:
            print("[ERROR] Cannot establish session - not registered!")
            return False

        print(f"\n[STEP] Establishing PDU session for {self.imsi}...")

        time.sleep(0.5)

        # Simulate IP allocation
        # In real network, SMF assigns this from pool (10.45.0.0/16)
        last_octet = int(self.imsi[-3:]) % 255 + 1
        self.ip_address = f"10.45.1.{last_octet}"

        print(f"[✓] PDU Session established!")
        print(f"    IP Address: {self.ip_address}")
        print(f"    DNN: {dnn}")
        return True

    def initiate_call(self, target_msisdn):
        """
        Initiate voice call to another phone

        Real Process (SIP/IMS signaling):
        1. Phone sends: SIP INVITE to target
        2. Target receives: Call notification (ringing)
        3. Target sends: SIP 180 Ringing
        4. Caller hears ringback tone

        Args:
            target_msisdn: Phone number to call

        Returns:
            Call object
        """
        print(f"\n[STEP] {self.msisdn} calling {target_msisdn}...")

        time.sleep(0.5)
        print(f"  [1/2] Sending call invitation...")
        time.sleep(0.5)
        print(f"  [2/2] Waiting for answer...")

        return Call(self.msisdn, target_msisdn)

    def answer_call(self):
        """
        Answer incoming call

        Real Process:
        1. Phone sends: SIP 200 OK
        2. Media (voice) path established
        3. Both parties can talk
        """
        print(f"[✓] {self.msisdn} answered the call")
        self.call_active = True
        return True

    def end_call(self):
        """End active call"""
        print(f"[✓] {self.msisdn} ended the call")
        self.call_active = False
        return True


class Call:
    """
    Represents an active voice call
    Monitors call quality metrics
    """

    def __init__(self, caller, callee):
        self.caller = caller
        self.callee = callee
        self.state = "ALERTING"  # States: ALERTING → ACTIVE → TERMINATED
        self.start_time = None
        self.end_time = None

        # Quality metrics
        self.mos = 4.0  # Mean Opinion Score (1-5, 5=best)
        self.packet_loss = 0.5  # Percentage
        self.jitter = 20  # Milliseconds
        self.latency = 30  # Milliseconds

    def answer(self):
        """Call is answered"""
        self.state = "ACTIVE"
        self.start_time = datetime.now()
        print(f"[✓] Call ACTIVE: {self.caller} ↔ {self.callee}")

    def get_metrics(self):
        """
        Get current call quality metrics

        Real metrics come from:
        - RTP (Real-time Transport Protocol) statistics
        - Jitter buffer monitoring
        - Packet loss detection

        We simulate realistic values
        """
        import random

        # Simulate realistic variations
        self.mos = round(random.uniform(3.8, 4.3), 2)
        self.packet_loss = round(random.uniform(0.1, 1.0), 2)
        self.jitter = round(random.uniform(15, 35), 1)
        self.latency = round(random.uniform(25, 45), 1)

        return {
            'mos': self.mos,
            'packet_loss': self.packet_loss,
            'jitter': self.jitter,
            'latency': self.latency
        }

    def terminate(self):
        """End the call"""
        self.state = "TERMINATED"
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        return duration


def test_voice_call(ue1_imsi, ue2_imsi, duration=60):
    """
    Complete voice call test

    Args:
        ue1_imsi: IMSI of first UE (caller)
        ue2_imsi: IMSI of second UE (callee)
        duration: Call duration in seconds

    Returns:
        Test results dictionary
    """
    print("="*70)
    print(" "*20 + "5G VOICE CALL TEST")
    print("="*70)

    # Step 1: Initialize UEs
    print("\n[PHASE 1] Initializing UEs...")
    ue1 = UESimulator(imsi=ue1_imsi)
    ue2 = UESimulator(imsi=ue2_imsi)

    # Step 2: Register both UEs
    print("\n[PHASE 2] Network Registration...")
    if not ue1.register():
        return {"success": False, "error": "UE1 registration failed"}

    if not ue2.register():
        return {"success": False, "error": "UE2 registration failed"}

    # Step 3: Establish PDU sessions (for IMS - voice over data)
    print("\n[PHASE 3] Establishing Data Sessions...")
    if not ue1.establish_pdu_session(dnn="ims"):
        return {"success": False, "error": "UE1 session failed"}

    if not ue2.establish_pdu_session(dnn="ims"):
        return {"success": False, "error": "UE2 session failed"}

    # Step 4: Initiate call
    print("\n[PHASE 4] Call Establishment...")
    call = ue1.initiate_call(ue2.msisdn)

    # Step 5: Answer call
    time.sleep(1)
    ue2.answer_call()
    call.answer()

    # Step 6: Monitor call quality
    print(f"\n[PHASE 5] Call Active - Monitoring for {duration} seconds...")
    print("\nCall Quality Metrics:")
    print(f"{'Time':<8} {'MOS':<8} {'Loss%':<10} {'Jitter(ms)':<12} {'Latency(ms)':<12}")
    print("-" * 60)

    metrics_history = []

    for i in range(duration):
        time.sleep(1)
        metrics = call.get_metrics()
        metrics_history.append(metrics)

        # Display every 5 seconds
        if (i + 1) % 5 == 0:
            print(f"{i+1:>4}s    {metrics['mos']:<8} "
                  f"{metrics['packet_loss']:<10} "
                  f"{metrics['jitter']:<12} "
                  f"{metrics['latency']:<12}")

    # Step 7: End call
    print("\n[PHASE 6] Terminating Call...")
    ue1.end_call()
    call_duration = call.terminate()

    # Calculate averages
    avg_mos = sum(m['mos'] for m in metrics_history) / len(metrics_history)
    avg_packet_loss = sum(m['packet_loss'] for m in metrics_history) / len(metrics_history)
    avg_jitter = sum(m['jitter'] for m in metrics_history) / len(metrics_history)
    avg_latency = sum(m['latency'] for m in metrics_history) / len(metrics_history)

    # Step 8: Test Results
    print("\n" + "="*70)
    print(" "*25 + "TEST RESULTS")
    print("="*70)

    print(f"\n✓ Call Successfully Completed")
    print(f"\nCall Details:")
    print(f"  Caller:    {ue1.msisdn} (IMSI: {ue1_imsi})")
    print(f"  Callee:    {ue2.msisdn} (IMSI: {ue2_imsi})")
    print(f"  Duration:  {call_duration:.1f} seconds")

    print(f"\nAverage Call Quality:")
    print(f"  MOS Score:       {avg_mos:.2f} / 5.00")
    print(f"  Packet Loss:     {avg_packet_loss:.2f}%")
    print(f"  Jitter:          {avg_jitter:.1f} ms")
    print(f"  Latency:         {avg_latency:.1f} ms")

    # Quality assessment
    print(f"\nQuality Assessment:")
    if avg_mos >= 4.0:
        print(f"  ✓ EXCELLENT - Call quality is excellent")
    elif avg_mos >= 3.5:
        print(f"  ✓ GOOD - Call quality is good")
    elif avg_mos >= 3.0:
        print(f"  ⚠ FAIR - Call quality is acceptable")
    else:
        print(f"  ✗ POOR - Call quality is poor")

    print("\n" + "="*70)

    results = {
        "success": True,
        "caller": ue1.msisdn,
        "callee": ue2.msisdn,
        "duration": call_duration,
        "avg_mos": avg_mos,
        "avg_packet_loss": avg_packet_loss,
        "avg_jitter": avg_jitter,
        "avg_latency": avg_latency
    }

    return results


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='5G Voice Call Testing')
    parser.add_argument('--ue1', required=True, help='IMSI of UE1 (caller)')
    parser.add_argument('--ue2', required=True, help='IMSI of UE2 (callee)')
    parser.add_argument('--duration', type=int, default=60,
                       help='Call duration in seconds (default: 60)')

    args = parser.parse_args()

    try:
        results = test_voice_call(args.ue1, args.ue2, args.duration)

        if results['success']:
            print("\n[SUCCESS] Voice call test completed successfully!")
            exit(0)
        else:
            print(f"\n[FAILED] {results.get('error', 'Unknown error')}")
            exit(1)

    except KeyboardInterrupt:
        print("\n\n[INFO] Test interrupted by user")
        exit(130)
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        exit(1)


if __name__ == '__main__':
    main()


# ============================================================================
# HOW TO USE THIS SCRIPT
# ============================================================================
#
# Basic Usage:
# ------------
# python voice_call_test.py --ue1 "001010000000001" --ue2 "001010000000002"
#
# With custom duration:
# ---------------------
# python voice_call_test.py \
#   --ue1 "001010000000001" \
#   --ue2 "001010000000002" \
#   --duration 120
#
# Expected Output:
# ----------------
# ======================================================================
#                      5G VOICE CALL TEST
# ======================================================================
#
# [PHASE 1] Initializing UEs...
# [INFO] Created UE: IMSI=001010000000001, Phone=+15550000001
# [INFO] Created UE: IMSI=001010000000002, Phone=+15550000002
#
# [PHASE 2] Network Registration...
# [STEP] Registering 001010000000001 to network...
#   [1/4] Sending Registration Request...
#   [2/4] Performing Authentication...
#   [3/4] Completing Security Setup...
#   [4/4] Receiving Registration Accept...
# [✓] 001010000000001 successfully registered!
#
# ... (similar for UE2)
#
# [PHASE 3] Establishing Data Sessions...
# [STEP] Establishing PDU session for 001010000000001...
# [✓] PDU Session established!
#     IP Address: 10.45.1.1
#     DNN: ims
#
# [PHASE 4] Call Establishment...
# [STEP] +15550000001 calling +15550000002...
#   [1/2] Sending call invitation...
#   [2/2] Waiting for answer...
# [✓] +15550000002 answered the call
# [✓] Call ACTIVE: +15550000001 ↔ +15550000002
#
# [PHASE 5] Call Active - Monitoring for 60 seconds...
#
# Call Quality Metrics:
# Time     MOS      Loss%      Jitter(ms)   Latency(ms)
# ------------------------------------------------------------
#    5s    4.12     0.45       22.3         32.1
#   10s    4.05     0.62       28.7         38.4
#   15s    4.18     0.38       19.2         29.8
# ...
#
# [PHASE 6] Terminating Call...
# [✓] +15550000001 ended the call
#
# ======================================================================
#                         TEST RESULTS
# ======================================================================
#
# ✓ Call Successfully Completed
#
# Call Details:
#   Caller:    +15550000001 (IMSI: 001010000000001)
#   Callee:    +15550000002 (IMSI: 001010000000002)
#   Duration:  60.0 seconds
#
# Average Call Quality:
#   MOS Score:       4.08 / 5.00
#   Packet Loss:     0.52%
#   Jitter:          24.3 ms
#   Latency:         33.7 ms
#
# Quality Assessment:
#   ✓ EXCELLENT - Call quality is excellent
#
# ======================================================================
#
# [SUCCESS] Voice call test completed successfully!
#
#
# ============================================================================
# WHAT THIS SCRIPT SIMULATES
# ============================================================================
#
# In a REAL 5G network, this script would:
#
# 1. Use actual 5G modems/phones
# 2. Send real NAS/NGAP messages to AMF
# 3. Establish real IMS sessions
# 4. Use SIP protocol for call signaling
# 5. Stream real voice using RTP
# 6. Monitor actual network KPIs
#
# For DEMONSTRATION purposes, we simulate:
# - UE behavior (registration, sessions)
# - Call establishment flow
# - Quality metrics (MOS, jitter, latency)
#
# This shows understanding of:
# - 5G call flows
# - Quality monitoring
# - Test automation
# - Network protocols
#
#
# ============================================================================
# MOS (Mean Opinion Score) EXPLAINED
# ============================================================================
#
# MOS is how we measure voice quality:
#
# Score    Quality     Description
# -----    -------     -----------
# 5.0      Excellent   Perfect quality, no issues
# 4.0-4.5  Good        High quality, barely noticeable issues
# 3.5-4.0  Fair        Acceptable quality, minor issues
# 3.0-3.5  Poor        Noticeable issues, but usable
# < 3.0    Bad         Unacceptable quality
#
# Factors affecting MOS:
# - Packet Loss: Lost voice packets = choppy audio
# - Jitter: Variation in packet arrival = robotic voice
# - Latency: Delay = conversation lag
# - Codec: G.711 (high quality) vs AMR (mobile optimized)
#
# Target for 5G voice calls: MOS > 4.0
