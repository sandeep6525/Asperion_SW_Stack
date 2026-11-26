"""
Unit & Integration Tests for Visual Analytics & Multi-Capable Dashboard API
"""
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.analytics import (
    get_executive_overview, get_financial_charts, get_delivery_charts,
    get_talent_charts, get_secops_charts, get_strategy_radar,
    simulate_cashflow, CashflowSimulationRequest,
    get_balanced_scorecard, get_workforce_intelligence,
    get_learning_intelligence, get_sharepoint_telemetry,
    get_predictive_models_telemetry, get_strategic_mcda_analysis,
    get_monte_carlo_risk_simulation, simulate_capital_allocation,
    CapitalAllocationSimulationRequest, get_executive_infographics
)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_analytics_executive_overview(db_session):
    data = get_executive_overview(db=db_session)
    assert data["status"] == "success"
    fin = data["financial_summary"]
    assert "total_invoiced_inr" in fin
    assert fin["total_invoiced_inr"] >= 500000.0
    assert "cash_runway_months" in fin
    assert fin["cash_runway_months"] > 0
    assert "net_operating_margin_pct" in fin
    assert "dso_days" in fin

    gov = data["governance_and_compliance"]
    assert gov["statutory_compliance_index_pct"] > 0
    assert gov["certin_sla_compliance_pct"] == 100.0

def test_analytics_financial_charts(db_session):
    data = get_financial_charts(db=db_session)
    cf = data["cashflow_time_series"]
    assert len(cf["labels"]) >= 13
    assert len(cf["inflows"]) >= 13
    assert len(cf["outflows"]) >= 13
    assert len(cf["closing_cash"]) >= 13

    aging = data["aging_analysis"]
    assert "0-30 Days (Current)" in aging["labels"]
    assert len(aging["accounts_receivable"]) == 4

    cost = data["cost_allocation"]
    assert len(cost["labels"]) >= 4

    tax = data["tax_matrix"]
    assert "output_gst_inr" in tax
    assert "net_gst_payable_inr" in tax

def test_analytics_delivery_charts(db_session):
    data = get_delivery_charts(db=db_session)
    vel = data["sprint_velocity"]
    assert len(vel["labels"]) >= 1
    assert len(vel["committed_points"]) == len(vel["completed_points"])

    raid = data["raid_risk_heatmap"]
    assert len(raid["labels"]) == 4

    tasks = data["task_pipeline"]
    assert "To Do" in tasks["labels"]
    assert "Done" in tasks["labels"]

def test_analytics_talent_charts(db_session):
    data = get_talent_charts(db=db_session)
    dept = data["department_headcount"]
    assert len(dept["labels"]) >= 1

    slabs = data["compensation_slabs"]
    assert len(slabs["labels"]) == 4

    comp = data["ctc_components_breakdown"]
    assert "Basic Salary (40%)" in comp["labels"]

def test_analytics_secops_charts(db_session):
    data = get_secops_charts(db=db_session)
    assert len(data["threat_vectors"]["labels"]) == 4
    sla = data["certin_sla_status"]
    assert sla["within_6hr_sla_pct"] == 100.0
    iam = data["iam_security_posture"]
    assert iam["passkey_adoption_pct"] > 0

def test_analytics_strategy_radar(db_session):
    data = get_strategy_radar(db=db_session)
    radar = data["maturity_radar"]
    assert len(radar["axes"]) == 6
    assert len(radar["scores"]) == 6
    for s in radar["scores"]:
        assert 0 <= s <= 100

def test_analytics_simulate_cashflow(db_session):
    req = CashflowSimulationRequest(
        collection_acceleration_pct=15.0,
        expense_optimization_pct=10.0,
        new_monthly_retainer_inr=300000.0
    )
    res = simulate_cashflow(req=req, db=db_session)
    assert res["status"] == "success"
    assert res["simulated_ending_cash_inr"] > res["baseline_ending_cash_inr"]
    assert res["cash_variance_delta_inr"] > 0
    assert len(res["chart_data"]["simulated_closing_balance"]) >= 13

def test_analytics_balanced_scorecard(db_session):
    data = get_balanced_scorecard(db=db_session)
    assert data["status"] == "success"
    assert data["corporate_entity"]["cin"] == "U85500KA2026OPC222069"
    assert data["corporate_entity"]["director"] == "Varadi Vijay"
    
    scorecard = data["scorecard"]
    assert "financial_perspective" in scorecard
    assert "customer_commercial_perspective" in scorecard
    assert "internal_process_perspective" in scorecard
    assert "learning_people_perspective" in scorecard

    countdown = data["statutory_countdown_radar"]
    assert len(countdown) >= 5
    assert any("MGT-7A" in item["name"] for item in countdown)
    assert any("TDS" in item["name"] for item in countdown)

def test_analytics_workforce_intelligence(db_session):
    data = get_workforce_intelligence(db=db_session)
    assert len(data["department_headcount"]["labels"]) >= 1
    assert len(data["ctc_slabs"]["labels"]) == 4
    assert len(data["attendance_health"]["labels"]) == 4
    assert len(data["recruitment_funnel"]["labels"]) == 6
    assert data["probation_status"]["clearance_rate_pct"] > 0

def test_analytics_learning_intelligence(db_session):
    data = get_learning_intelligence(db=db_session)
    assert len(data["department_hours"]["labels"]) >= 1
    assert data["department_hours"]["min_required_threshold"] == 16.0
    assert len(data["quiz_score_distribution"]["labels"]) == 4
    assert len(data["top_materials"]) >= 1

def test_analytics_sharepoint_telemetry(db_session):
    data = get_sharepoint_telemetry(db=db_session)
    assert data["total_articles"] >= 1
    assert data["total_knowledge_reads"] >= 1
    assert data["community_questions"]["total"] >= 1
    assert data["community_questions"]["resolution_rate_pct"] > 0

def test_analytics_predictive_models(db_session):
    data = get_predictive_models_telemetry(db=db_session)
    assert data["status"] == "success"
    rev = data["revenue_forecast"]
    assert len(rev["historical_labels"]) == 6
    assert len(rev["forecast_labels"]) == 6
    assert len(rev["forecast_mean"]) == 6
    assert len(rev["forecast_upper_95"]) == 6
    assert len(rev["forecast_lower_95"]) == 6
    # Upper bound should strictly exceed mean
    for mean, upper in zip(rev["forecast_mean"], rev["forecast_upper_95"]):
        assert upper > mean

    churn = data["customer_churn_analytics"]
    assert len(churn["clients"]) >= 4
    assert churn["average_churn_probability_pct"] > 0
    assert "DSO Payment Lag Days" in churn["feature_importance"]

    ml = data["ml_model_telemetry"]
    assert ml["accuracy_pct"] > 90.0
    assert ml["f1_score"] > 0.90
    assert ml["roc_auc"] > 0.95
    assert ml["confusion_matrix"]["true_positive"] > 0

def test_analytics_strategic_mcda(db_session):
    data = get_strategic_mcda_analysis(db=db_session)
    assert data["status"] == "success"
    assert data["corporate_entity"] == "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED"
    assert data["director"] == "Varadi Vijay"
    assert len(data["criteria_weights"]) == 5
    assert len(data["ranked_initiatives"]) == 4
    assert data["ranked_initiatives"][0]["priority_rank"] == 1
    assert data["ranked_initiatives"][0]["composite_mcda_score"] >= data["ranked_initiatives"][1]["composite_mcda_score"]
    assert "top_recommendation" in data
    assert "decision_rationale" in data

def test_analytics_monte_carlo(db_session):
    data = get_monte_carlo_risk_simulation(db=db_session)
    assert data["status"] == "success"
    assert data["simulation_parameters"]["total_iterations"] == 1000
    sched = data["schedule_distribution"]
    assert len(sched["labels"]) == 8
    assert len(sched["frequency"]) == 8
    assert sched["cumulative_prob_pct"][-1] == 100.0

    percentiles = data["schedule_percentiles"]
    assert percentiles["p95_contractual_sla_days"] > percentiles["p50_expected_days"]
    assert percentiles["p80_high_confidence_days"] >= percentiles["p50_expected_days"]

    budget = data["budget_risk_var"]
    assert budget["p95_worst_case_budget_inr"] > budget["baseline_budget_inr"]
    assert budget["value_at_risk_95_inr"] > 0

def test_analytics_simulate_capital_allocation(db_session):
    req = CapitalAllocationSimulationRequest(
        headcount_additions=4,
        ai_compute_budget_monthly_inr=300000.0,
        enterprise_sales_spend_inr=200000.0,
        pricing_tier_adjustment_pct=15.0
    )
    res = simulate_capital_allocation(req=req, db=db_session)
    assert res["status"] == "success"
    treasury = res["treasury_impact"]
    assert treasury["new_monthly_burn_inr"] > 350000.0
    assert treasury["simulated_runway_months"] > 0

    growth = res["growth_and_unit_economics"]
    assert growth["projected_arr_inr"] > 9300000.0
    assert growth["rule_of_40_score"] > 0
    assert "ltv_to_cac_ratio" in growth

    rec = res["executive_recommendation"]
    assert rec["director"] == "Varadi Vijay"
    assert rec["flag"] in ["OPTIMAL_EXPANSION", "BALANCED_PRUDENT", "CAPITAL_CONSTRAINED"]

def test_analytics_executive_infographics(db_session):
    data = get_executive_infographics(db=db_session)
    assert data["status"] == "success"
    assert data["entity"]["cin"] == "U85500KA2026OPC222069"
    assert data["entity"]["director"] == "Varadi Vijay"
    assert data["composite_health_index"]["score"] > 90.0
    assert len(data["key_infographics"]) >= 6
    assert any("Rule of 40" in item["title"] for item in data["key_infographics"])
    assert any("Zero-Trust" in item["title"] for item in data["key_infographics"])
