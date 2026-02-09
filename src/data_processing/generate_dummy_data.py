"""
Generate realistic dummy insurance plan data
"""

import json
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from typing import Dict, List


class DummyDataGenerator:
    """Generate realistic insurance plan PDFs and JSON files"""
    
    def __init__(self, output_dir: str = "data/dummy_dataset"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.plans = self._define_plans()
    
    def _define_plans(self) -> List[Dict]:
        """Define 3 realistic insurance plans"""
        return [
            {
                'plan_name': 'BlueCross HMO Blue New England',
                'provider': 'Blue Cross Blue Shield MA',
                'plan_type': 'HMO',
                'year': '2025',
                'monthly_premium': 450,
                'deductible': 1500,
                'out_of_pocket_max': 6000,
                'benefits': {
                    'Primary Care Visit': 'You pay $25 copay per visit',
                    'Specialist Visit': 'You pay $50 copay per visit. Referral required.',
                    'Emergency Room': 'You pay $350 copay per visit. Waived if admitted.',
                    'Urgent Care': 'You pay $50 copay per visit. No referral needed.',
                    'Preventive Care': 'No charge. Annual physical exam, immunizations, and screenings covered 100%.',
                    'Laboratory Tests': 'You pay $15 copay for lab work at Quest or LabCorp.',
                    'X-rays and Imaging': 'You pay $75 copay. Prior authorization required for MRI/CT.',
                    'Outpatient Surgery': 'You pay 20% coinsurance after deductible.',
                    'Inpatient Hospital': 'You pay $500 copay per admission.',
                    'Mental Health Outpatient': 'You pay $25 copay per visit, same as primary care.',
                    'Physical Therapy': 'You pay $40 copay per visit. Maximum 30 visits per year.',
                    'Prescription Drugs Generic': 'You pay $10 copay for 30-day supply.',
                    'Prescription Drugs Brand': 'You pay $40 copay for preferred brand, $70 for non-preferred.',
                    'Vision Exam': 'No charge. One routine exam per year covered.',
                    'Dental Preventive': 'No charge. Two cleanings per year covered.',
                    'Gym Membership': 'SilverSneakers program included at no additional cost.',
                    'Telehealth': 'No charge for virtual primary care visits.',
                }
            },
            {
                'plan_name': 'BlueCross PPO Blue',
                'provider': 'Blue Cross Blue Shield MA',
                'plan_type': 'PPO',
                'year': '2025',
                'monthly_premium': 550,
                'deductible': 2000,
                'out_of_pocket_max': 7000,
                'benefits': {
                    'Primary Care Visit': 'You pay $30 copay in-network. Out-of-network: deductible then 30% coinsurance.',
                    'Specialist Visit': 'You pay $60 copay in-network. No referral needed. Out-of-network: deductible then 30%.',
                    'Emergency Room': 'You pay $400 copay. Same cost in and out-of-network.',
                    'Urgent Care': 'You pay $60 copay in-network. Out-of-network: deductible then 30%.',
                    'Preventive Care': 'No charge in-network for ACA-covered preventive services.',
                    'Laboratory Tests': 'You pay $20 copay in-network.',
                    'X-rays and Imaging': 'You pay $100 copay in-network. No prior authorization needed.',
                    'Outpatient Surgery': 'You pay 20% coinsurance in-network after deductible.',
                    'Inpatient Hospital': 'You pay $750 copay per admission in-network.',
                    'Mental Health Outpatient': 'You pay $30 copay in-network.',
                    'Physical Therapy': 'You pay $45 copay per visit. Maximum 35 visits per year.',
                    'Prescription Drugs Generic': 'You pay $15 copay for 30-day supply.',
                    'Prescription Drugs Brand': 'You pay $50 preferred, $90 non-preferred.',
                    'Vision Exam': 'You pay $10 copay. One exam per year.',
                    'Gym Membership': '$25 monthly reimbursement for qualified fitness centers.',
                    'Telehealth': 'You pay $10 copay for virtual visits.',
                }
            },
            {
                'plan_name': 'Tufts Medicare Preferred HMO',
                'provider': 'Tufts Health Plan',
                'plan_type': 'Medicare Advantage HMO',
                'year': '2025',
                'monthly_premium': 0,
                'deductible': 0,
                'out_of_pocket_max': 4500,
                'benefits': {
                    'Primary Care Visit': 'No charge for PCP visits.',
                    'Specialist Visit': 'You pay $25 copay. Referral required.',
                    'Emergency Room': 'You pay $90 copay. Covered worldwide.',
                    'Urgent Care': 'You pay $25 copay. No referral needed.',
                    'Preventive Care': 'No charge for Medicare-covered preventive services.',
                    'Annual Wellness Visit': 'No charge. Includes personalized prevention plan.',
                    'Laboratory Tests': 'No charge for covered lab services.',
                    'X-rays and Imaging': 'You pay $50 copay for diagnostic imaging.',
                    'Outpatient Surgery': 'You pay $250 copay per procedure.',
                    'Inpatient Hospital': 'You pay $325 copay per day for days 1-5 per admission.',
                    'Skilled Nursing Facility': 'No charge for days 1-20. You pay $196/day for days 21-100.',
                    'Home Health Care': 'No charge for Medicare-covered home health services.',
                    'Mental Health Outpatient': 'You pay $25 copay for individual therapy.',
                    'Physical Therapy': 'You pay $25 copay when medically necessary.',
                    'Cardiac Rehabilitation': 'You pay $25 copay when medically necessary.',
                    'Prescription Drugs Tier 1': 'You pay $3 copay for preferred generic drugs.',
                    'Prescription Drugs Tier 2': 'You pay $10 copay for generic drugs.',
                    'Prescription Drugs Tier 3': 'You pay $47 copay for preferred brand drugs.',
                    'Vision Exam': 'No charge. One routine exam per year.',
                    'Eyewear Allowance': '$200 allowance every year for glasses or contacts.',
                    'Dental Preventive': 'No charge. Two cleanings, exams, and x-rays per year.',
                    'Dental Comprehensive': '$1,000 annual maximum for fillings, extractions, crowns.',
                    'Hearing Exam': 'No charge. One exam per year.',
                    'Hearing Aids': '$2,000 allowance per year for both ears.',
                    'Gym Membership': 'SilverSneakers fitness program included.',
                    'Over-the-Counter': '$75 quarterly allowance for OTC health items.',
                    'Transportation': '24 one-way trips per year to medical appointments.',
                    'Telehealth': 'No charge for primary care and behavioral health virtual visits.',
                    'Acupuncture for Chronic Pain': 'You pay $25 copay. Up to 20 visits per year.',
                    'Meal Delivery': '14 meals delivered after hospital discharge.',
                    'In-Home Support': '40 hours of support services after hospital discharge.',
                }
            },
        ]
    
    def generate_pdf(self, plan: Dict) -> Path:
        """Generate PDF document for a plan"""
        filename = f"{plan['provider'].replace(' ', '_')}_{plan['plan_name'].replace(' ', '_')}.pdf"
        filepath = self.output_dir / filename
        
        c = canvas.Canvas(str(filepath), pagesize=letter)
        width, height = letter
        
        # Title page
        y = height - inch
        c.setFont("Helvetica-Bold", 20)
        c.drawString(inch, y, plan['plan_name'])
        y -= 0.4 * inch
        
        c.setFont("Helvetica", 14)
        c.drawString(inch, y, f"{plan['provider']}")
        y -= 0.3 * inch
        c.drawString(inch, y, f"Plan Year {plan['year']}")
        y -= 0.5 * inch
        
        # Plan overview
        c.setFont("Helvetica-Bold", 12)
        c.drawString(inch, y, "PLAN OVERVIEW")
        y -= 0.25 * inch
        
        c.setFont("Helvetica", 10)
        overview = [
            f"Plan Type: {plan['plan_type']}",
            f"Monthly Premium: ${plan['monthly_premium']}",
            f"Annual Deductible: ${plan['deductible']}",
            f"Out-of-Pocket Maximum: ${plan['out_of_pocket_max']}"
        ]
        
        for line in overview:
            c.drawString(inch, y, line)
            y -= 0.2 * inch
        
        y -= 0.3 * inch
        
        # Benefits section
        c.setFont("Helvetica-Bold", 12)
        c.drawString(inch, y, "COVERED SERVICES AND COST SHARING")
        y -= 0.3 * inch
        
        for service, cost in plan['benefits'].items():
            # Check if we need a new page
            if y < 2 * inch:
                c.showPage()
                y = height - inch
            
            c.setFont("Helvetica-Bold", 9)
            c.drawString(inch, y, service)
            y -= 0.15 * inch
            
            c.setFont("Helvetica", 8)
            # Text wrapping
            words = cost.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                if c.stringWidth(test_line, "Helvetica", 8) < (width - 2.5 * inch):
                    line = test_line
                else:
                    c.drawString(inch + 0.2*inch, y, line.strip())
                    y -= 0.13 * inch
                    line = word + " "
            if line:
                c.drawString(inch + 0.2*inch, y, line.strip())
                y -= 0.15 * inch
            
            y -= 0.1 * inch
        
        c.save()
        return filepath
    
    def generate_json(self, plan: Dict) -> Path:
        """Generate JSON file for a plan"""
        filename = f"{plan['provider'].replace(' ', '_')}_{plan['plan_name'].replace(' ', '_')}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(plan, f, indent=2)
        
        return filepath
    
    def generate_all(self):
        """Generate all plan documents"""
        print("🏗️  Generating dummy insurance dataset...\n")
        
        for plan in self.plans:
            print(f"Creating: {plan['plan_name']}")
            pdf_path = self.generate_pdf(plan)
            json_path = self.generate_json(plan)
            
            print(f"  ✅ PDF: {pdf_path.name}")
            print(f"  ✅ JSON: {json_path.name}\n")
        
        print(f"🎉 Successfully generated {len(self.plans)} insurance plans!")
        print(f"📁 Saved to: {self.output_dir}\n")
        
        # Show what was created
        print("📄 Files created:")
        for file in sorted(self.output_dir.glob("*")):
            print(f"  - {file.name}")


if __name__ == "__main__":
    generator = DummyDataGenerator()
    generator.generate_all()