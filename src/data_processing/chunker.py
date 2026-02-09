"""
Create semantic chunks from extracted data
"""

import json
from pathlib import Path
from typing import Dict, List


class BenefitChunker:
    """Create searchable chunks from benefits"""
    
    def __init__(self):
        # Categories help with filtering and better search
        self.categories = {
            'preventive': ['preventive', 'screening', 'wellness', 'annual', 'physical', 'immunization'],
            'emergency': ['emergency', 'urgent', 'ambulance'],
            'hospital': ['hospital', 'inpatient', 'admission', 'surgery', 'outpatient'],
            'prescription': ['prescription', 'drug', 'pharmacy', 'medication', 'tier'],
            'dental': ['dental', 'teeth', 'cleaning', 'orthodont', 'crown', 'filling'],
            'vision': ['vision', 'eye', 'glasses', 'contacts', 'exam', 'eyewear'],
            'mental_health': ['mental', 'therapy', 'counseling', 'behavioral', 'psychiatrist', 'psychologist'],
            'therapy': ['physical therapy', 'occupational', 'speech', 'rehabilitation', 'cardiac'],
            'specialist': ['specialist', 'consultation', 'referral'],
            'primary_care': ['primary care', 'pcp', 'doctor visit'],
            'wellness': ['gym', 'fitness', 'silversneakers', 'wellness', 'weight loss'],
            'telehealth': ['telehealth', 'virtual', 'telemedicine'],
            'transportation': ['transportation', 'rides', 'trip'],
            'hearing': ['hearing', 'hearing aid', 'audiologist'],
            'home_health': ['home health', 'home care', 'home support'],
            'meals': ['meal', 'food', 'nutrition'],
            'otc': ['over-the-counter', 'otc'],
        }
    
    def chunk_file(self, json_path: str) -> List[Dict]:
        """Create chunks from one extracted JSON file"""
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        chunks = []
        
        # Create overview chunk
        overview = self._create_overview(data['metadata'])
        chunks.append(overview)
        
        # Create benefit chunks
        for benefit in data.get('benefits', []):
            chunk = self._create_benefit_chunk(benefit, data['metadata'])
            chunks.append(chunk)
        
        return chunks
    
    def _create_overview(self, metadata: Dict) -> Dict:
        """Create a plan overview chunk"""
        parts = []
        
        plan = metadata.get('plan_name', 'This plan')
        provider = metadata.get('provider', '')
        
        parts.append(f"{plan} is offered by {provider}.")
        
        if 'plan_type' in metadata:
            parts.append(f"This is a {metadata['plan_type']} plan.")
        
        if 'monthly_premium' in metadata:
            premium = metadata['monthly_premium']
            if premium == 0:
                parts.append(f"This plan has no monthly premium ($0).")
            else:
                parts.append(f"The monthly premium is ${premium}.")
        
        if 'deductible' in metadata:
            deductible = metadata['deductible']
            if deductible == 0:
                parts.append(f"This plan has no deductible ($0).")
            else:
                parts.append(f"The annual deductible is ${deductible}.")
        
        text = " ".join(parts)
        
        return {
            'text': text,
            'type': 'overview',
            'category': 'general',
            **metadata
        }
    
    def _create_benefit_chunk(self, benefit: Dict, metadata: Dict) -> Dict:
        """Create a chunk for one benefit"""
        service = benefit['service']
        description = benefit['description']
        
        # Create natural language text
        text = f"For {service}: {description}"
        
        # Add plan context
        if 'plan_name' in metadata:
            text = f"Under the {metadata['plan_name']}, {text.lower()}"
        
        # Classify category
        category = self._classify(service.lower() + " " + description.lower())
        
        return {
            'text': text,
            'service': service,
            'description': description,
            'type': 'benefit',
            'category': category,
            **metadata
        }
    
    def _classify(self, text: str) -> str:
        """Classify benefit into a category"""
        scores = {}
        
        for category, keywords in self.categories.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[category] = score
        
        # Return category with highest score
        if scores:
            return max(scores, key=scores.get)
        
        return 'general'
    
    def process_all(self, input_dir: str = "data/processed"):
        """Process all extracted JSON files"""
        input_path = Path(input_dir)
        json_files = list(input_path.glob("*_extracted.json"))
        
        if not json_files:
            print("❌ No extracted JSON files found in data/processed/")
            print("   Please run pdf_extractor.py first!")
            return []
        
        print(f"📦 Creating chunks from {len(json_files)} files...\n")
        
        all_chunks = []
        
        for json_file in json_files:
            print(f"  Processing: {json_file.name}")
            chunks = self.chunk_file(str(json_file))
            all_chunks.extend(chunks)
            print(f"    ✅ Created {len(chunks)} chunks")
        
        # Save all chunks
        output_file = input_path / "all_chunks.json"
        with open(output_file, 'w') as f:
            json.dump(all_chunks, f, indent=2)
        
        print(f"\n✅ Total chunks created: {len(all_chunks)}")
        print(f"💾 Saved to: {output_file}\n")
        
        # Print statistics
        self._print_statistics(all_chunks)
        
        return all_chunks
    
    def _print_statistics(self, chunks: List[Dict]):
        """Print statistics about chunks"""
        print("📊 Chunk Statistics:")
        
        # Count by category
        categories = {}
        for chunk in chunks:
            cat = chunk.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n  By Category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"    {cat:20s}: {count}")
        
        # Count by plan
        plans = {}
        for chunk in chunks:
            plan = chunk.get('plan_name', 'unknown')
            plans[plan] = plans.get(plan, 0) + 1
        
        print("\n  By Plan:")
        for plan, count in plans.items():
            print(f"    {plan}: {count} chunks")


if __name__ == "__main__":
    chunker = BenefitChunker()
    chunker.process_all()