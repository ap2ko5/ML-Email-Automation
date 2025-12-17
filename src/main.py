#!/usr/bin/env python3
"""
ML-Email-Automation Main Entry Point

This module serves as the main entry point for the email automation system.
It orchestrates email checking, model prediction, and automation execution.
"""

import argparse
import logging
from datetime import datetime
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler

from src.email_handler import EmailHandler
from src.automation_engine import AutomationEngine
from src.model_predictor import ModelPredictor
from src.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)


class EmailAutomationSystem:
    """Main system orchestrator for email automation"""

    def __init__(self, config_path: str = None):
        """Initialize the automation system"""
        self.email_handler = EmailHandler(config_path)
        self.automation_engine = AutomationEngine()
        self.model_predictor = ModelPredictor()
        self.scheduler = BackgroundScheduler()
        logger.info("Email Automation System initialized")

    def process_emails(self):
        """Process emails and participate in legitimate giveaways"""
        try:
            logger.info("Starting email processing cycle")
            
            # Fetch unread giveaway emails
            emails = self.email_handler.fetch_emails(
                label='Giveaway',
                unread_only=True
            )
            logger.info(f"Fetched {len(emails)} unread emails")

            for email in emails:
                try:
                    # Extract email features
                    email_text = self._extract_email_text(email)
                    
                    # Predict legitimacy using ML model
                    prediction = self.model_predictor.predict(email_text)
                    confidence = self.model_predictor.get_confidence_score(email_text)
                    
                    logger.info(
                        f"Email '{email.get('subject')}' - "
                        f"Legitimate: {prediction}, Confidence: {confidence:.2%}"
                    )
                    
                    # Only participate if legitimacy confidence is high
                    if prediction and confidence > 0.85:
                        logger.info(f"Attempting to participate in giveaway")
                        self.automation_engine.participate_in_giveaway(email)
                    else:
                        logger.debug(f"Skipping email - low confidence")
                        
                except Exception as e:
                    logger.error(f"Error processing email: {str(e)}", exc_info=True)
                    continue
            
            logger.info("Email processing cycle completed")
            
        except Exception as e:
            logger.error(f"Critical error during email processing: {str(e)}", exc_info=True)

    def start_scheduler(self, interval: int = 3600):
        """Start the background scheduler
        
        Args:
            interval: Time interval in seconds between email checks
        """
        self.scheduler.add_job(
            self.process_emails,
            'interval',
            seconds=interval,
            id='email_processor',
            name='Email Processing Job'
        )
        self.scheduler.start()
        logger.info(f"Scheduler started with {interval}s interval")

    def stop_scheduler(self):
        """Stop the background scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")

    def run_once(self):
        """Run email processing once"""
        self.process_emails()

    @staticmethod
    def _extract_email_text(email: dict) -> str:
        """Extract and combine relevant text from email
        
        Args:
            email: Email dictionary
            
        Returns:
            Combined email text
        """
        subject = email.get('subject', '')
        body = email.get('body', '')
        return f"{subject}\n{body}"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='ML-powered Email Automation System'
    )
    parser.add_argument(
        '--mode',
        choices=['auto', 'once'],
        default='once',
        help='Execution mode: auto (scheduled) or once (single run)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=3600,
        help='Interval in seconds between email checks (auto mode)'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level'
    )

    args = parser.parse_args()

    # Initialize system
    system = EmailAutomationSystem(config_path=args.config)

    try:
        if args.mode == 'auto':
            logger.info(f"Starting in AUTO mode with {args.interval}s interval")
            system.start_scheduler(interval=args.interval)
            
            # Keep running
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received interrupt signal")
                system.stop_scheduler()
                logger.info("System shutting down gracefully")
        else:
            logger.info("Running in ONCE mode")
            system.run_once()
            logger.info("Single run completed")
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
