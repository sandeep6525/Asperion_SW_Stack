import re

with open("E:/Asperion_SW_Stack/Asperion_SW_Stack/Asperion_SW_Stack/asperion_stack/frontend/src/utils/dataLoaders.js", "r", encoding="utf-8") as f:
    text = f.read()

def find_ids(start_str, end_str):
    start = text.find(start_str)
    if start == -1: return []
    end = text.find(end_str, start)
    if end == -1: end = start + 5000
    part = text[start:end]
    return re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", part)

print("SecOps IDs:", find_ids("export async function loadSecOps()", "export async function loadSecOpsAnalytics()"))
print("ITSM IDs:", find_ids("export async function loadITSM()", "export function switchAgenticAITab("))
print("Vault IDs:", find_ids("export async function loadVault()", "export async function loadStrategy()"))
print("Teams IDs:", find_ids("export async function loadTeams()", "export function escapeHtml("))
print("SharePoint IDs:", find_ids("export async function loadSharePoint()", "export async function loadTraining()"))
print("Training IDs:", find_ids("export async function loadTraining()", "export async function loadBalancedScorecard()"))
