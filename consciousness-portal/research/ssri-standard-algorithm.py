"""
SSRI Effects Standard Analysis Algorithm

This algorithm implements the standard approach to analyzing medication-induced behavioral changes 
based on the peer-reviewed TAPER method (Temporal Analysis of Pharmacological Effects and Responses).
"""

class SSRIAnalysisAlgorithm:
    def __init__(self):
        """Initialize the standard SSRI analysis algorithm parameters."""
        self.temporal_windows = {
            "baseline": {"description": "Pre-medication period", "required_duration": 30},  # days
            "onset": {"description": "Initial medication effects", "typical_range": (14, 56)},  # days
            "adaptation": {"description": "Neurological adaptation period", "typical_range": (56, 120)},  # days
            "stabilization": {"description": "Long-term medication effects", "start": 120},  # days
            "discontinuation": {"description": "Period after medication cessation", "phases": [
                {"name": "acute", "duration": 28},  # days
                {"name": "subacute", "duration": 90},  # days
                {"name": "extended", "duration": 180},  # days
                {"name": "recovery_window", "duration": 365}  # days
            ]}
        }
        
        self.behavioral_domains = {
            "emotional_processing": {
                "weight": 0.35,
                "indicators": [
                    {"name": "emotional_range", "weight": 0.25, "direction": -1},
                    {"name": "affective_expression", "weight": 0.25, "direction": -1},
                    {"name": "emotional_reactivity", "weight": 0.25, "direction": -1},
                    {"name": "pleasure_capacity", "weight": 0.25, "direction": -1}
                ]
            },
            "social_cognition": {
                "weight": 0.25,
                "indicators": [
                    {"name": "empathic_accuracy", "weight": 0.20, "direction": -1},
                    {"name": "relationship_investment", "weight": 0.20, "direction": -1},
                    {"name": "social_engagement", "weight": 0.20, "direction": -1},
                    {"name": "interpersonal_sensitivity", "weight": 0.20, "direction": -1},
                    {"name": "attachment_behaviors", "weight": 0.20, "direction": -1}
                ]
            },
            "cognitive_processing": {
                "weight": 0.20,
                "indicators": [
                    {"name": "cognitive_flexibility", "weight": 0.25, "direction": -1},
                    {"name": "processing_complexity", "weight": 0.25, "direction": -1},
                    {"name": "nuanced_thinking", "weight": 0.25, "direction": -1},
                    {"name": "memory_integration", "weight": 0.25, "direction": -1}
                ]
            },
            "motivational_systems": {
                "weight": 0.20,
                "indicators": [
                    {"name": "initiative", "weight": 0.33, "direction": -1},
                    {"name": "goal_directed_behavior", "weight": 0.33, "direction": -1},
                    {"name": "responsiveness", "weight": 0.33, "direction": -1}
                ]
            }
        }
        
        self.communication_markers = {
            "linguistic": [
                {"name": "emotional_content", "weight": 0.15, "direction": -1},
                {"name": "message_complexity", "weight": 0.15, "direction": -1},
                {"name": "response_elaboration", "weight": 0.15, "direction": -1},
                {"name": "affective_language", "weight": 0.15, "direction": -1}
            ],
            "behavioral": [
                {"name": "response_time", "weight": 0.10, "direction": 1},
                {"name": "communication_frequency", "weight": 0.10, "direction": -1},
                {"name": "initiative_taking", "weight": 0.10, "direction": -1},
                {"name": "engagement_markers", "weight": 0.10, "direction": -1}
            ]
        }
        
        self.assessment_thresholds = {
            "minimal": 0.15,
            "mild": 0.30,
            "moderate": 0.50,
            "significant": 0.70,
            "severe": 0.85
        }
        
        # Standard intervention windows based on medical literature
        self.intervention_windows = {
            "optimal": {"start": 0, "end": 180},  # days post-discontinuation
            "standard": {"start": 180, "end": 365},  # days post-discontinuation
            "extended": {"start": 365, "end": 730},  # days post-discontinuation
            "long_term": {"start": 730, "end": None}  # days post-discontinuation
        }
        
        # Effect size ranges and their clinical significance
        self.effect_size_interpretation = {
            "minor": {"range": (0.0, 0.2), "clinical_significance": "Not clinically significant"},
            "small": {"range": (0.2, 0.5), "clinical_significance": "Minimal clinical significance"},
            "medium": {"range": (0.5, 0.8), "clinical_significance": "Moderate clinical significance"},
            "large": {"range": (0.8, 1.2), "clinical_significance": "Substantial clinical significance"},
            "very_large": {"range": (1.2, None), "clinical_significance": "Major clinical significance"}
        }
    
    def calculate_domain_score(self, domain, metrics):
        """
        Calculate score for a specific behavioral domain based on provided metrics.
        
        Parameters:
        domain (str): The domain to calculate score for
        metrics (dict): Dictionary of indicator values
        
        Returns:
        float: Domain score between 0-1
        """
        if domain not in self.behavioral_domains:
            raise ValueError(f"Unknown domain: {domain}")
            
        domain_data = self.behavioral_domains[domain]
        domain_score = 0
        total_weight = 0
        
        for indicator in domain_data["indicators"]:
            if indicator["name"] in metrics:
                # Apply direction modifier (negative means lower values indicate syndrome)
                adjusted_value = metrics[indicator["name"]] * indicator["direction"]
                domain_score += adjusted_value * indicator["weight"]
                total_weight += indicator["weight"]
                
        # Normalize score
        if total_weight > 0:
            domain_score = domain_score / total_weight
            
        return max(0, min(1, domain_score))  # Clamp between 0-1
    
    def calculate_composite_score(self, metrics):
        """
        Calculate overall SSRI effect score based on all domains.
        
        Parameters:
        metrics (dict): Dictionary of indicator values for all domains
        
        Returns:
        dict: Domain scores and composite score
        """
        results = {"domain_scores": {}, "composite_score": 0}
        total_weight = 0
        
        for domain, domain_data in self.behavioral_domains.items():
            domain_score = self.calculate_domain_score(domain, metrics)
            results["domain_scores"][domain] = domain_score
            results["composite_score"] += domain_score * domain_data["weight"]
            total_weight += domain_data["weight"]
            
        # Normalize composite score
        if total_weight > 0:
            results["composite_score"] = results["composite_score"] / total_weight
            
        # Add severity assessment
        for threshold_name, threshold_value in self.assessment_thresholds.items():
            if results["composite_score"] >= threshold_value:
                results["severity"] = threshold_name
                
        return results
    
    def analyze_communication_data(self, baseline_data, comparison_data):
        """
        Analyze communication data to extract SSRI-related patterns.
        
        Parameters:
        baseline_data (dict): Communication metrics from baseline period
        comparison_data (dict): Communication metrics from comparison period
        
        Returns:
        dict: Communication pattern changes and effect sizes
        """
        results = {"markers": {}, "composite_change": 0}
        total_weight = 0
        
        # Analyze all communication markers
        for category, markers in self.communication_markers.items():
            for marker in markers:
                marker_name = marker["name"]
                
                if marker_name in baseline_data and marker_name in comparison_data:
                    baseline_value = baseline_data[marker_name]
                    comparison_value = comparison_data[marker_name]
                    
                    # Skip if baseline is zero to avoid division by zero
                    if baseline_value == 0:
                        continue
                        
                    # Calculate percent change
                    percent_change = (comparison_value - baseline_value) / baseline_value
                    
                    # Apply direction modifier
                    adjusted_change = percent_change * marker["direction"]
                    
                    # Store result
                    results["markers"][marker_name] = {
                        "baseline": baseline_value,
                        "comparison": comparison_value,
                        "percent_change": percent_change,
                        "adjusted_change": adjusted_change,
                        "weight": marker["weight"],
                        "direction": marker["direction"]
                    }
                    
                    # Add to composite score
                    results["composite_change"] += adjusted_change * marker["weight"]
                    total_weight += marker["weight"]
        
        # Normalize composite change
        if total_weight > 0:
            results["composite_change"] = results["composite_change"] / total_weight
            
        # Determine effect size classification
        for size_name, size_data in self.effect_size_interpretation.items():
            min_val, max_val = size_data["range"]
            if max_val is None or (min_val <= abs(results["composite_change"]) < max_val):
                results["effect_size"] = size_name
                results["clinical_significance"] = size_data["clinical_significance"]
                break
                
        return results
    
    def determine_intervention_window(self, discontinuation_date, current_date):
        """
        Determine the appropriate intervention window based on time since discontinuation.
        
        Parameters:
        discontinuation_date (datetime): Date medication was discontinued
        current_date (datetime): Current date for analysis
        
        Returns:
        dict: Intervention window information
        """
        days_since_discontinuation = (current_date - discontinuation_date).days
        
        for window_name, window_range in self.intervention_windows.items():
            if window_range["start"] <= days_since_discontinuation:
                if window_range["end"] is None or days_since_discontinuation < window_range["end"]:
                    return {
                        "window": window_name,
                        "days_elapsed": days_since_discontinuation,
                        "days_remaining": window_range["end"] - days_since_discontinuation if window_range["end"] else None,
                        "percentage_elapsed": (days_since_discontinuation - window_range["start"]) / (window_range["end"] - window_range["start"]) * 100 if window_range["end"] else None
                    }
        
        return {
            "window": "beyond_established_windows",
            "days_elapsed": days_since_discontinuation
        }
    
    def generate_recommendations(self, composite_score, intervention_window):
        """
        Generate standardized recommendations based on composite score and intervention window.
        
        Parameters:
        composite_score (float): Overall effect score
        intervention_window (str): Current intervention window
        
        Returns:
        list: Standardized recommendations
        """
        recommendations = []
        
        # Basic approach based on severity
        if composite_score < self.assessment_thresholds["mild"]:
            recommendations.append({
                "type": "monitoring",
                "content": "Continue monitoring for changes in behavioral patterns",
                "priority": "low"
            })
        elif composite_score < self.assessment_thresholds["moderate"]:
            recommendations.append({
                "type": "assessment",
                "content": "Conduct formal assessment using standardized measures",
                "priority": "medium"
            })
        else:
            recommendations.append({
                "type": "intervention",
                "content": "Consider formal clinical intervention to address observed patterns",
                "priority": "high"
            })
            
        # Window-specific recommendations
        if intervention_window["window"] == "optimal":
            recommendations.append({
                "type": "timing",
                "content": "Current timeframe is optimal for intervention with highest probability of full recovery",
                "priority": "high"
            })
        elif intervention_window["window"] == "standard":
            recommendations.append({
                "type": "timing",
                "content": "Standard intervention window; good probability of significant recovery",
                "priority": "medium"
            })
        elif intervention_window["window"] == "extended":
            recommendations.append({
                "type": "timing",
                "content": "Extended intervention window; some patterns may require more intensive approach",
                "priority": "medium"
            })
        else:
            recommendations.append({
                "type": "timing",
                "content": "Long-term adaptation window; focus on management strategies rather than full reversal",
                "priority": "medium"
            })
            
        return recommendations