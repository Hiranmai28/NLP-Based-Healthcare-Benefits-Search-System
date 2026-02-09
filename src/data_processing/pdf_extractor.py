"""
Extract structured data from insurance PDFs
"""

import pdfplumber
import re
import json
from pathlib import Path
from typing import Dict, List


class PDFExtractor:
    """Extract text and structure from insurance PDFs"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.data = {
            'metadata': {},
            'benefits': [],
            'full_text': ''
        }
    
    def extract(self) -> Dict:
        """Main extraction method"""
        print(f"  📄 Extracting: {self.pdf_path.name}")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            # Extract metadata from first page
            first_page = pdf.pages[0].extract_text()
            self.data['metadata'] = self._extract_metadata(first_page)
            
            # Extract all text
            full_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)
            
            self.data['full_text'] = '\n\n'.join(full_text)
            
            # Extract individual benefits
            self.data['benefits'] = self._extract_benefits(self.data['full_text'])
        
        print(f"    ✅ Found {len(self.data['benefits'])} benefits")
        return self.data
    
    def _extract_metadata(self, text: str) -> Dict:
        """Extract plan metadata from first page"""
        metadata = {}
        
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        # Plan name (usually first line)
        if lines:
            metadata['plan_name'] = lines[0]
        
        # Provider
        providers = ['Blue Cross', 'Harvard Pilgrim', 'Tufts', 'Fallon', 'WellSense']
        for line in lines[:10]:
            for provider in providers:
                if provider in line:
                    metadata['provider'] = line
                    break
        
        # Year
        year_match = re.search(r'20\d{2}', text)
        if year_match:
            metadata['year'] = year_match.group()
        
        # Plan type
        for ptype in ['HMO', 'PPO', 'EPO', 'HDHP', 'Medicare Advantage', 'Medicaid']:
            if ptype in text:
                metadata['plan_type'] = ptype
                break
        
        # Costs
        premium_patterns = [
            r'Premium[:\s]*\$(\d+)',
            r'Monthly Premium[:\s]*\$(\d+)',
        ]
        for pattern in premium_patterns:
            premium_match = re.search(pattern, text, re.IGNORECASE)
            if premium_match:
                metadata['monthly_premium'] = int(premium_match.group(1))
                break
        
        deductible_patterns = [
            r'Deductible[:\s]*\$(\d+)',
            r'Annual Deductible[:\s]*\$(\d+)',
        ]
        for pattern in deductible_patterns:
            deductible_match = re.search(pattern, text, re.IGNORECASE)
            if deductible_match:
                metadata['deductible'] = int(deductible_match.group(1))
                break
        
        return metadata
    
    def _extract_benefits(self, text: str) -> List[Dict]:
        """Extract individual benefits with descriptions"""
        benefits = []
        
        lines = text.split('\n')
        current_service = None
        current_description = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip section headers
            if line in ['PLAN OVERVIEW', 'COVERED SERVICES', 'COVERED SERVICES AND COST SHARING']:
                continue
            
            # Check if this is a service header (benefit name)
            if self._is_service_header(line):
                # Save previous benefit
                if current_service and current_description:
                    benefits.append({
                        'service': current_service,
                        'description': ' '.join(current_description)
                    })
                
                current_service = line
                current_description = []
            else:
                # This is description text
                if current_service:
                    current_description.append(line)
        
        # Save last benefit
        if current_service and current_description:
            benefits.append({
                'service': current_service,
                'description': ' '.join(current_description)
            })
        
        return benefits
    
    def _is_service_header(self, line: str) -> bool:
        """Detect if a line is a benefit service name"""
        # Service headers are usually short and contain service keywords
        
        if len(line) > 80:
            return False
        
        if line.lower().startswith('you pay'):
            return False
        
        if line.startswith('Plan Type:') or line.startswith('Monthly Premium:'):
            return False
        
        service_keywords = [
            'visit', 'care', 'exam', 'test', 'therapy', 'surgery',
            'hospital', 'prescription', 'drug', 'vision', 'dental',
            'menttal', 'physical', 'emergency', 'urgent', 'preventive',
            'laboratory', 'x-ray', 'imaging', 'outpatient', 'inpatient',
            'gym', 'membership', 'telehealth', 'transportation', 'wellness',
            'hearing', 'eyewear', 'allowance', 'meal', 'support', 'acupuncture',
            'tier', 'rehabilitation', 'skilled', 'home health', 'over-the-counter'
        ]
        
        line_lower = line.lower()
        return any(keyword in line_lower for keyword in service_keywords)
    
    def save(self, output_dir: str = "data/processed"):
        """Save extracted data as JSON"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filename = self.pdf_path.stem + "_extracted.json"
        filepath = output_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=2)

        print(f"    💾 Saved: {filename}")
        return filepath


def extract_all_pdfs(input_dir: str = "data/dummy_dataset"):
    """Process all PDFs in directory"""
    input_path = Path(input_dir)
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in data/dummy_dataset/")
        print("   Please run generate_dummy_data.py first!")
        return []
    
    print(f"📚 Extracting text from {len(pdf_files)} PDFs...\n")

    extracted_files = []
    for pdf_file in pdf_files:
        try:
            extractor = PDFExtractor(pdf_file)
            extractor.extract()
            output = extractor.save()
            extracted_files.append(output)
            print()
        except Exception as e:
            print(f"    ❌ Error processing {pdf_file.name}: {e}\n")
    
    print(f"🎉 Extraction complete! Processed {len(extracted_files)} files")
    print(f"📁 Saved to: data/processed/\n")
    
    # List what was created
    print("📄 Extracted files:")
    for file in extracted_files:
        print(f"  - {file.name}")
    
    return extracted_files


if __name__ == "__main__":
    extract_all_pdfs()
        