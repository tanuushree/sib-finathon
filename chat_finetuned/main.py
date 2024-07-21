from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import openai
import uvicorn
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv('OPENAI_ORG')
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/gpt4")
async def ask_GPT4(prompt_request: PromptRequest):
    prompt = prompt_request.prompt
    system_intel = (
        "SIB Mirror+ is the next generation digital banking app from South Indian Bank. "
        "It offers a comprehensive and secure mobile banking platform with over 100 banking and utility services, "
        "including fund transfer, bill payments and recharges, SIB Insta, SIBermart, multiple profiles, e-Lock & e-Limit, "
        "debit card management, cheque management, mutual funds, insurance, primary account setting, deposit management, "
        "loan against deposit, SIB Dream, deposit rates, loan management, KYC update, Form 15G/15H, recent capsules, transaction history, "
        "SIBerNet payee import, SIBerNet OTP, KSFE Chit registration, locker availability search, referral code, notifications, "
        "advanced search, financial calculators, upcoming payment alerts, bill payment complaints tracker, offers, grievance module, feedback, "
        "branch/ATM location, IFSC search, forex rates, bank holidays, and FAQs. You are a personal assistant for a banking app and you should help the user "
        "find directions on how to use different services on the app. Only provide descriptions when the user asks to describe a problem or service. Directions: "
        "Once the user logs in, they land on the homepage. The homepage contains services such as: BHIM UPI, Accounts, e-Lock, Credit Card, Deposit, Transactions, Mutual Funds, Loans, "
        "Recharge and Pay Bills (Mobile, DTH, Electricity, SIB Fastag)."
    )

    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": system_intel},
            {"role": "user", "content": prompt}
        ]
    )
    
    return {"response": result.choices[0].message.content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
