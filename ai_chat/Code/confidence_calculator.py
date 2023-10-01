from utils import extract_from_response
from retriever import get_highest_similarity_score
from logger import setup_logger

logger = setup_logger(__name__)  # Configure logging

class ConfidenceCalculator:
    # Constants for component weights
    PRIMARY_INTENT_WEIGHT = 0.20
    SECONDARY_INTENT_WEIGHT = 0.15
    ENTITY_WEIGHT = 0.20
    AGENT_WEIGHT = 0.20
    SEMANTIC_WEIGHT = 0.10
    DOMAIN_SPECIFICITY_WEIGHT = 0.15

    def __init__(self, known_agents):
        self.known_agents = known_agents

    def calculate_confidence(self, input_query, output, specialist_agent, log=True):
        parsed_response = extract_from_response(output)
        primary_intent = parsed_response.get('primary_intent', '')
        secondary_intents = parsed_response.get('secondary_intent', [])
        extracted_entities = parsed_response.get('entities', [])
        
        # Intent Confidence
        primary_intent_confidence = self._calculate_intent_confidence(primary_intent)
        
        # Secondary Intent Confidence
        secondary_intent_confidence = self._calculate_intent_confidence(secondary_intents)
        
        # Semantic Confidence
        semantic_confidence = self._calculate_semantic_confidence(input_query)
        
        # Entity Confidence
        entity_confidence = self._calculate_entity_confidence(extracted_entities)
        
        # Specialist Agent Confidence
        agent_confidence = self._calculate_agent_confidence(specialist_agent)
        
        # Domain-Specificity Confidence
        domain_specificity = self._calculate_domain_specificity(input_query)
        
        # Overall confidence with new metric
        confidence = self._calculate_overall_confidence(primary_intent_confidence, semantic_confidence, secondary_intent_confidence, entity_confidence, agent_confidence, domain_specificity)
        
        if log:
            logger.info(f"Individual Components: Semantic: {semantic_confidence}, Primary: {primary_intent_confidence}, Entity: {entity_confidence}")
            logger.info(f"Confidence components: {semantic_confidence}, {primary_intent_confidence}, {entity_confidence}")
            logger.info(f"Calculated confidence for query '{input_query}': {confidence}")
        
        return confidence

    def _calculate_intent_confidence(self, intent):
        return 1.0 if intent else 0.0

    def _calculate_semantic_confidence(self, input_query):
        similarity_score = get_highest_similarity_score(input_query)
        return similarity_score  # Use the raw score

    def _calculate_entity_confidence(self, entities):
        return 1.0 if entities else 0.0

    def _calculate_agent_confidence(self, agent):
        return 1.0 if agent in self.known_agents else 0.0

    def _calculate_domain_specificity(self, input_query):
        similarity_score = get_highest_similarity_score(input_query)
        return 1.0 if similarity_score > 0.7 else 0.0

    def _calculate_overall_confidence(self, primary_intent_confidence, semantic_confidence, secondary_intent_confidence, entity_confidence, agent_confidence, domain_specificity):
        confidence = (self.PRIMARY_INTENT_WEIGHT * primary_intent_confidence +
                      self.SEMANTIC_WEIGHT * semantic_confidence +
                      self.SECONDARY_INTENT_WEIGHT * secondary_intent_confidence +
                      self.ENTITY_WEIGHT * entity_confidence +
                      self.AGENT_WEIGHT * agent_confidence +
                      self.DOMAIN_SPECIFICITY_WEIGHT * domain_specificity)
        
        # Clip to valid range [0, 1]
        return max(0.0, min(1.0, confidence))