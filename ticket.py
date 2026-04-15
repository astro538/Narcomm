import streamlit as st

st.set_page_config(page_title="AI Helpdesk Assistant", layout="centered")

st.title("🤖 AI Helpdesk Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

if st.session_state.clear_input:
    st.session_state.user_issue_input = ""
    st.session_state.clear_input = False

if "ticket_counter" not in st.session_state:
    st.session_state.ticket_counter = 0

# Function to simulate AI (replace later with ML + Ollama)
def process_ticket(text):
    # Dummy logic (replace later)
    if "internet" in text.lower():
        category = "Network"
        priority = "High"
        confidence = 0.85
        solution = "Restart router, check cables, and update drivers."
    elif "login" in text.lower():
        category = "Application"
        priority = "Medium"
        confidence = 0.65
        solution = "Reset password and clear cache."
    else:
        category = "General"
        priority = "Low"
        confidence = 0.45
        solution = "Please provide more details."

    # Status logic
    status = "Resolved ✅" if confidence >= 0.6 else "Escalated ⚠"

    return category, priority, confidence, solution, status

interface = st.sidebar.radio(
    "Select interface",
    ["User Interface", "Service Team Interface"],
)

if interface == "User Interface":
    # Input box
    st.subheader("📝 Enter your issue")
    user_input = st.text_area("Describe your issue:", key="user_issue_input")

    # Button
    if st.button("Analyze Ticket 🚀"):
        if user_input.strip() != "":
            category, priority, confidence, solution, status = process_ticket(user_input)
            st.session_state.ticket_counter += 1

            # Save to ticket history
            st.session_state.messages.append({
                "id": st.session_state.ticket_counter,
                "user": user_input,
                "category": category,
                "priority": priority,
                "confidence": confidence,
                "solution": solution,
                "status": status,
                "feedback": "Not Reviewed",
                "escalation_locked": False,
                "escalated_by": "System" if status == "Escalated ⚠" else "None",
            })

            # Clear input on next rerun before widget is instantiated.
            st.session_state.clear_input = True
            st.rerun()

    # Display conversation
    st.subheader("💬 Conversation")

    if not st.session_state.messages:
        st.info("No analyzed tickets yet. Enter an issue above and click Analyze Ticket.")

    for idx, msg in enumerate(st.session_state.messages):
        msg.setdefault("id", idx + 1)
        msg.setdefault("feedback", "Not Reviewed")
        msg.setdefault("escalation_locked", False)
        msg.setdefault("escalated_by", "System" if msg.get("status") == "Escalated ⚠" else "None")

        st.markdown(f"**🎫 Ticket #{msg['id']}**")
        st.markdown(f"**👤 User:** {msg['user']}")

        with st.container():
            st.markdown("**🤖 AI Response**")

            if msg["confidence"] > 0.75:
                conf_color = "🟢"
            elif msg["confidence"] > 0.5:
                conf_color = "🟡"
            else:
                conf_color = "🔴"

            st.markdown(
                f"📊 **Analysis**\n"
                f"- Category: **{msg['category']}**\n"
                f"- Priority: **{msg['priority']}**\n"
                f"- Confidence: **{conf_color} {msg['confidence']:.2f}**\n\n"
                f"💡 **Solution**\n"
                f"{msg['solution']}"
            )

            feedback_options = ["Not Reviewed", "Helpful", "Not Helpful"]
            selected_feedback = st.radio(
                "Was this suggested solution helpful?",
                options=feedback_options,
                index=feedback_options.index(msg["feedback"]),
                key=f"feedback_{msg['id']}",
                horizontal=True,
                disabled=msg["escalation_locked"],
            )

            if not msg["escalation_locked"] and selected_feedback != msg["feedback"]:
                msg["feedback"] = selected_feedback
                if selected_feedback == "Not Helpful":
                    msg["status"] = "Escalated ⚠"
                    msg["escalation_locked"] = True
                    msg["escalated_by"] = "User Feedback"
                elif selected_feedback == "Helpful":
                    msg["status"] = "Resolved ✅"
                    msg["escalated_by"] = "None"

            st.markdown(f"⚙️ **Status**\n**{msg['status']}**")
            st.caption(f"Feedback: {msg['feedback']}")

            if msg["escalation_locked"]:
                st.warning("This ticket was escalated after user feedback and is now locked.")

            st.markdown("---")

else:
    st.subheader("🛠️ Service Team Dashboard")
    escalated_tickets = [
        msg for msg in st.session_state.messages if msg.get("status") == "Escalated ⚠"
    ]

    if not escalated_tickets:
        st.success("No escalated tickets at the moment.")
    else:
        st.write(f"Showing {len(escalated_tickets)} escalated ticket(s)")
        for msg in escalated_tickets:
            ticket_id = msg.get("id", "N/A")
            with st.container():
                st.markdown(f"**🎫 Ticket #{ticket_id}**")
                st.markdown(f"- Category: **{msg['category']}**")
                st.markdown(f"- Priority: **{msg['priority']}**")
                st.markdown(f"- Escalated By: **{msg.get('escalated_by', 'System')}**")
                st.markdown(f"- User Feedback: **{msg.get('feedback', 'Not Reviewed')}**")
                st.markdown("**Issue**")
                st.write(msg["user"])
                st.markdown("**Suggested Solution Sent To User**")
                st.write(msg["solution"])
                st.markdown("---")