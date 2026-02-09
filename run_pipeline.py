"""
Simple Q&A interface for Healthcare Benefits Navigator
"""

from src.models.retriever import BenefitRetriever
from typing import List, Dict


class HealthcareChatbot:
    """Interactive chatbot for insurance benefits"""
    
    def __init__(self):
        print("🤖 Initializing Healthcare Benefits Navigator...")
        self.retriever = BenefitRetriever()
        print()
    
    def ask(self, question: str, show_details: bool = True) -> str:
        """
        Ask a question and get an answer
        
        Args:
            question: User's question
            show_details: Whether to show detailed results
        
        Returns:
            Answer text
        """
        print(f"\n❓ Question: {question}\n")
        
        # Search for relevant chunks
        results = self.retriever.search(question, top_k=3)
        
        if not results:
            return "❌ I couldn't find any information about that."
        
        # Display results
        print("📋 Found these relevant benefits:\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['plan_name']}")
            print(f"   {result['text']}")
            
            if show_details:
                print(f"   📊 Similarity: {result['similarity_score']:.1%}")
                print(f"   🏷️  Category: {result['category']}")
            
            print()
        
        return results
    
    def compare_plans_for_benefit(self, benefit_query: str):
        """Compare how different plans cover a specific benefit"""
        print(f"\n🔍 Comparing plans for: {benefit_query}\n")
        
        plans = self.retriever.list_plans()
        comparison = {}
        
        for plan in plans:
            results = self.retriever.search(benefit_query, top_k=1, plan_filter=plan)
            if results:
                comparison[plan] = results[0]
        
        if not comparison:
            print("❌ No information found for any plan.")
            return
        
        print("📊 Comparison:\n")
        for plan, result in comparison.items():
            print(f"• {plan}:")
            print(f"  {result['description']}")
            print()
    
    def list_available_plans(self):
        """Show all available plans"""
        plans = self.retriever.list_plans()
        
        print("\n📋 Available Plans:\n")
        for i, plan in enumerate(plans, 1):
            print(f"{i}. {plan}")
            
            # Get overview
            overview = self.retriever.get_plan_overview(plan)
            if overview:
                print(f"   {overview['text']}")
            print()
    
    def show_statistics(self):
        """Display index statistics"""
        stats = self.retriever.get_statistics()
        
        print("\n📊 System Statistics:\n")
        print(f"Total Plans: {stats['total_plans']}")
        print(f"Total Benefits Indexed: {stats['total_chunks']}")
        print(f"Benefit Categories: {len(stats['categories'])}")
        print()
        
        print("Plans:")
        for plan, count in stats['chunks_by_plan'].items():
            print(f"  • {plan}: {count} benefits")
        print()
    
    def interactive_mode(self):
        """Run interactive Q&A session"""
        print("="*60)
        print("🏥 HEALTHCARE BENEFITS NAVIGATOR")
        print("="*60)
        print()
        print("Ask me anything about your health insurance benefits!")
        print("Type 'quit' to exit, 'plans' to see available plans")
        print("Type 'compare: <benefit>' to compare plans")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Stay healthy!")
                    break
                
                if user_input.lower() == 'plans':
                    self.list_available_plans()
                    continue
                
                if user_input.lower() == 'stats':
                    self.show_statistics()
                    continue
                
                if user_input.lower().startswith('compare:'):
                    benefit = user_input[8:].strip()
                    self.compare_plans_for_benefit(benefit)
                    continue
                
                # Regular question
                self.ask(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


def demo_queries():
    """Run demo with sample queries"""
    print("="*60)
    print("🎬 DEMO: Healthcare Benefits Navigator")
    print("="*60)
    print()
    
    chatbot = HealthcareChatbot()
    
    # Demo questions
    demo_questions = [
        "Does my plan cover gym membership?",
        "What's the copay for seeing a specialist?",
        "Is preventive care covered?",
        "How much do prescription drugs cost?",
        "Does the plan include dental coverage?",
    ]
    
    print("🎯 Running demo queries...\n")
    
    for question in demo_questions:
        chatbot.ask(question, show_details=True)
        print("-" * 60)
    
    # Show plan comparison
    print("\n" + "="*60)
    chatbot.compare_plans_for_benefit("gym membership")
    print("="*60)
    
    # Show statistics
    chatbot.show_statistics()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Run demo
        demo_queries()
    else:
        # Run interactive mode
        chatbot = HealthcareChatbot()
        chatbot.interactive_mode()