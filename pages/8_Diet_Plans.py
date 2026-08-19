import streamlit as st
import pandas as pd

from services.patient_service import fetch_all_patients


from services.diet_plan_service import (
    create_new_diet_plan,
    add_meal_to_plan,
    fetch_diet_plans,
    fetch_diet_plan,
    fetch_diet_plan_meals,
    update_meal,
    delete_meal,
    update_plan_status,
    delete_existing_diet_plan,
    apply_diet_plan_template
)


from services.diet_plan_template_service import (
    get_template_names,
    get_diet_plan_template,
    get_template_summary
)


from services.diet_history_service import (
    fetch_patient_diet_history,
    get_patient_history_summary
)

from components import (
    load_theme,
    navbar,
    app_sidebar,
    footer
)

from utils.diet_plan_pdf_generator import generate_diet_plan_pdf

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Diet Plans",
    page_icon="🥗",
    layout="wide"
)


# ==========================================================
# DIET PLAN SESSION STATE
# ==========================================================

if "current_diet_plan_id" not in st.session_state:
    st.session_state.current_diet_plan_id = None


# ==========================================================
# THEME & NAVIGATION
# ==========================================================

load_theme()
app_sidebar()

navbar(
    "Diet Plans",
    "Patient Nutrition Planning"
)


# ==========================================================
# PAGE HEADER
# ==========================================================

st.subheader("🥗 Diet Plan Management")

st.write(
    "Create and manage personalized nutrition plans "
    "for patients."
)

# ==========================================================
# DIET PLAN DASHBOARD
# ==========================================================

st.markdown("---")

st.markdown(
    "## 📊 Diet Plan Dashboard"
)

try:

    all_diet_plans = fetch_diet_plans()

    # ======================================================
    # CALCULATE STATUS COUNTS
    # ======================================================

    total_plans = len(all_diet_plans)

    active_plans = sum(
        1
        for plan in all_diet_plans
        if (plan[4] or "Active") == "Active"
    )

    paused_plans = sum(
        1
        for plan in all_diet_plans
        if (plan[4] or "Active") == "Paused"
    )

    completed_plans = sum(
        1
        for plan in all_diet_plans
        if (plan[4] or "Active") == "Completed"
    )

    archived_plans = sum(
        1
        for plan in all_diet_plans
        if (plan[4] or "Active") == "Archived"
    )

    # ======================================================
    # UNIQUE PATIENTS
    # ======================================================

    unique_patients = len(
        set(
            plan[1]
            for plan in all_diet_plans
            if plan[1]
        )
    )

    # ======================================================
    # KPI CARDS
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📋 Total Plans",
            total_plans
        )

    with col2:

        st.metric(
            "🟢 Active",
            active_plans
        )

    with col3:

        st.metric(
            "⏸️ Paused",
            paused_plans
        )

    with col4:

        st.metric(
            "✅ Completed",
            completed_plans
        )

    col5, col6 = st.columns(2)

    with col5:

        st.metric(
            "📦 Archived",
            archived_plans
        )

    with col6:

        st.metric(
            "👥 Patients With Plans",
            unique_patients
        )

    # ======================================================
    # STATUS DISTRIBUTION
    # ======================================================

    if total_plans > 0:

        st.markdown(
            "### 📈 Plan Status Distribution"
        )

        status_data = {
            "Active": active_plans,
            "Paused": paused_plans,
            "Completed": completed_plans,
            "Archived": archived_plans
        }

        st.bar_chart(
            status_data
        )

    else:

        st.info(
            "ℹ️ No diet plans have been created yet."
        )

except Exception as error:

    st.error(
        f"❌ Unable to load diet plan dashboard: {error}"
    )



# ==========================================================
# LOAD PATIENTS
# ==========================================================

patients = fetch_all_patients()

patient_names = [
    patient.name
    for patient in patients
]


# ==========================================================
# PLAN INFORMATION
# ==========================================================

st.markdown("## 📋 Diet Plan Information")

col1, col2 = st.columns(2)


# ==========================================================
# PATIENT SELECTION
# ==========================================================

with col1:

    if patient_names:

        patient_name = st.selectbox(
            "👤 Select Patient",
            patient_names,
            index=None,
            placeholder="Select a patient..."
        )

    else:

        patient_name = None

        st.warning(
            "⚠️ No patients found. Please add a patient first."
        )


# ==========================================================
# PLAN NAME
# ==========================================================

with col2:

    plan_name = st.text_input(
        "📄 Plan Name",
        placeholder="e.g. Weight Gain Plan"
    )



# ==========================================================
# DIET PLAN SCHEDULE
# ==========================================================

st.markdown("### 📅 Diet Plan Schedule")

schedule_col1, schedule_col2 = st.columns(2)

with schedule_col1:

    start_date = st.date_input(
        "📅 Start Date",
        value=__import__("datetime").date.today(),
        key="new_plan_start_date"
    )

with schedule_col2:

    end_date = st.date_input(
        "📅 End Date",
        value=start_date,
        min_value=start_date,
        key="new_plan_end_date"
    )

duration_days = (
    end_date - start_date
).days + 1

st.info(
    f"⏱️ Diet Plan Duration: **{duration_days} days**"
)


# ==========================================================
# START NEW DIET PLAN
# ==========================================================

if st.button(
    "📋 Start New Diet Plan",
    use_container_width="stretch"
):

    if not patient_name:

        st.warning(
            "⚠️ Please select a patient."
        )

    elif not plan_name.strip():

        st.warning(
            "⚠️ Please enter a diet plan name."
        )

    else:

        try:

            diet_plan_id = create_new_diet_plan(
                patient_name,
                plan_name,
                start_date.isoformat(),
                end_date.isoformat(),
                duration_days
            )

            st.session_state.current_diet_plan_id = (
                diet_plan_id
            )

            st.success(
                f"✅ Diet plan created for {patient_name}!"
            )

        except ValueError as error:

            st.warning(
                f"⚠️ {error}"
            )

        except Exception as error:

            st.error(
                f"❌ Something went wrong: {error}"
            )


# ==========================================================
# EXISTING DIET PLANS
# ==========================================================


st.markdown("## 📂 Existing Diet Plans")

try:

    # ======================================================
    # LOAD ALL DIET PLANS
    # ======================================================

    all_existing_plans = fetch_diet_plans()

    # ======================================================
    # SEARCH & FILTER
    # ======================================================

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:

        search_text = st.text_input(
            "🔍 Search",
            placeholder="Patient or plan name..."
        )

    with filter_col2:

        status_filter = st.selectbox(
            "📌 Status",
            [
                "All",
                "Active",
                "Paused",
                "Completed",
                "Archived"
            ]
        )

    with filter_col3:

        patient_filter_options = ["All"]

        patient_filter_options += sorted(
            list(
                set(
                    plan[1]
                    for plan in all_existing_plans
                    if plan[1]
                )
            )
        )

        patient_filter = st.selectbox(
            "👤 Patient",
            patient_filter_options
        )

    # ======================================================
    # FILTER PLANS
    # ======================================================

    filtered_plans = []

    for plan in all_existing_plans:

        plan_id = plan[0]
        patient_name_saved = plan[1]
        plan_name_saved = plan[2]
        created_at = plan[3]
        status = plan[4] or "Active"

        # ==============================================
        # SEARCH FILTER
        # ==============================================

        if search_text.strip():

            search_value = search_text.strip().lower()

            patient_match = (
                search_value
                in str(patient_name_saved).lower()
            )

            plan_match = (
                search_value
                in str(plan_name_saved).lower()
            )

            if not patient_match and not plan_match:
                continue

        # ==============================================
        # STATUS FILTER
        # ==============================================

        if status_filter != "All":

            if status != status_filter:
                continue

        # ==============================================
        # PATIENT FILTER
        # ==============================================

        if patient_filter != "All":

            if patient_name_saved != patient_filter:
                continue

        filtered_plans.append(
            plan
        )

    # ======================================================
    # RESULT COUNT
    # ======================================================

    st.caption(
        f"Showing {len(filtered_plans)} "
        f"of {len(all_existing_plans)} diet plans"
    )

    # ======================================================
    # PLAN SELECTION
    # ======================================================

    if filtered_plans:

        plan_options = {}

        for plan in filtered_plans:

            plan_id = plan[0]
            patient_name_saved = plan[1]
            plan_name_saved = plan[2]
            created_at = plan[3]
            status = plan[4] or "Active"

            label = (
                f"{plan_name_saved} | "
                f"{patient_name_saved} | "
                f"{status} | "
                f"Created: {created_at}"
            )

            plan_options[label] = plan_id

        selected_plan_label = st.selectbox(
            "📋 Select Diet Plan",
            list(plan_options.keys()),
            index=None,
            placeholder="Select a saved diet plan..."
        )

        # ==================================================
        # LOAD SELECTED PLAN
        # ==================================================

        if selected_plan_label:

            selected_plan_id = plan_options[
                selected_plan_label
        ]

        st.session_state.current_diet_plan_id = (
            selected_plan_id
        )

    else:

        st.info(
            "ℹ️ No diet plans match your filters."
        )

except Exception as error:

    st.error(
        f"❌ Unable to load diet plans: {error}"
    )

# ==========================================================
# DIET PLAN STATUS
# ==========================================================

if st.session_state.current_diet_plan_id:

    st.markdown("---")

    st.markdown(
        "### 📌 Diet Plan Status"
    )

    try:

        current_plan = fetch_diet_plan(
            st.session_state.current_diet_plan_id
        )

        if current_plan:

            current_status = (
                current_plan[4]
                if current_plan[4]
                else "Active"
            )

            current_updated = (
                current_plan[5]
                if current_plan[5]
                else "Not updated yet"
            )

            status_col1, status_col2 = st.columns(2)

            with status_col1:

                st.info(
                    f"Current Status: **{current_status}**"
                )

            with status_col2:

                st.caption(
                    f"Last Updated: {current_updated}"
                )

                # ==================================================
                # DIET PLAN SCHEDULE
                # ==================================================

                st.markdown("#### 📅 Diet Plan Schedule")

                schedule_col1, schedule_col2, schedule_col3 = st.columns(3)

                with schedule_col1:

                    st.metric(
                        "📅 Start Date",
                        current_plan[6] or "Not set"
                    )

                with schedule_col2:

                    st.metric(
                    "📅 End Date",
                    current_plan[7] or "Not set"
                    )

                with schedule_col3:

                    st.metric(
                        "⏱️ Duration",
                        f"{current_plan[8]} days"
                        if current_plan[8]
                        else "Not set"
                    )

            new_status = st.selectbox(
                "Change Status",
                [
                    "Active",
                    "Paused",
                    "Completed",
                    "Archived"
                ],
                index=[
                    "Active",
                    "Paused",
                    "Completed",
                    "Archived"
                ].index(current_status),
                key="diet_plan_status"
            )

            if st.button(
                "💾 Update Plan Status",
                width="stretch"
            ):

                try:

                    update_plan_status(
                        st.session_state.current_diet_plan_id,
                        new_status
                    )

                    st.success(
                        f"✅ Diet plan marked as {new_status}."
                    )

                    st.rerun()

                except ValueError as error:

                    st.warning(
                        f"⚠️ {error}"
                    )

                except Exception as error:

                    st.error(
                        f"❌ Unable to update status: {error}"
                    )

    except Exception as error:

        st.error(
            f"❌ Unable to load plan status: {error}"
        )


# ==================================================
# DELETE DIET PLAN
# ==================================================

st.markdown("---")

if st.button(
    "🗑️ Delete This Diet Plan",
    width="stretch",
    key="delete_current_diet_plan"
):

    try:

        deleted_result = delete_existing_diet_plan(
            st.session_state.current_diet_plan_id
        )

        deleted_plan = deleted_result["deleted_plan"]
        deleted_meals = deleted_result["deleted_meals"]

        if deleted_plan:

            st.session_state.current_diet_plan_id = None

            st.success(
                f"✅ Diet plan deleted successfully. "
                f"Removed {deleted_meals} meal(s)."
            )

            st.rerun()

        else:

            st.warning(
                "⚠️ Diet plan was not found."
            )

    except ValueError as error:

        st.warning(
            f"⚠️ {error}"
        )

    except Exception as error:

        st.error(
            f"❌ Unable to delete diet plan: {error}"
        )

# ==========================================================
# DIET PLAN PDF EXPORT
# ==========================================================

st.markdown("---")

st.markdown(
    "### 📄 Diet Plan Report"
)

pdf_col1, pdf_col2 = st.columns(2)

with pdf_col1:

    generate_pdf = st.button(
        "📄 Generate Diet Plan PDF",
        use_container_width="stretch"
    )

with pdf_col2:

    st.caption(
        "Generate a professional PDF containing "
        "the complete diet plan and nutrition summary."
    )

if generate_pdf:

    try:

        pdf_filename = (
            f"diet_plan_{current_plan[0]}.pdf"
        )

        generate_diet_plan_pdf(
            current_plan,
            fetch_diet_plan_meals(
                st.session_state.current_diet_plan_id
            ),
            pdf_filename
        )

        with open(
            pdf_filename,
            "rb"
        ) as pdf_file:

            pdf_data = pdf_file.read()

        st.success(
            "✅ Diet plan PDF generated successfully!"
        )

        st.download_button(
            label="⬇️ Download Diet Plan PDF",
            data=pdf_data,
            file_name=pdf_filename,
            mime="application/pdf",
            use_container_width="stretch"
        )

    except Exception as error:

        st.error(
            f"❌ Unable to generate PDF: {error}"
        )

# ==========================================================
# DIET PLAN TEMPLATES
# ==========================================================

st.markdown("---")

st.markdown(
    "## 🧩 Diet Plan Templates"
)

template_col1, template_col2 = st.columns([2, 1])

with template_col1:

    template_names = get_template_names()

    selected_template = st.selectbox(
        "📋 Choose a Template",
        template_names,
        index=None,
        placeholder="Select a diet plan template..."
    )


# ==========================================================
# APPLY SELECTED TEMPLATE
# ==========================================================

if selected_template:

    if st.session_state.current_diet_plan_id:

        if st.button(
            "📋 Apply Template to Current Diet Plan",
            width="stretch",
            key="apply_template_button"
        ):

            try:

                added_meals = apply_diet_plan_template(
                    st.session_state.current_diet_plan_id,
                    selected_template
                )

                st.success(
                    f"✅ {len(added_meals)} meals from "
                    f"'{selected_template}' added successfully!"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"❌ Unable to apply template: {error}"
                )

    else:

        st.warning(
            "⚠️ Please create or select a diet plan first."
        )

with template_col2:

    if selected_template:

        template_summary = get_template_summary(
            selected_template
        )

        st.metric(
            "🍽️ Meals",
            template_summary["total_meals"]
        )

        st.metric(
            "🔥 Calories",
            f"{template_summary['total_calories']} kcal"
        )




# ==========================================================
# TEMPLATE PREVIEW
# ==========================================================

if selected_template:

    template_data = get_diet_plan_template(
        selected_template
    )

    st.info(
        template_data["description"]
    )

    preview_meals = template_data["meals"]

    st.markdown(
        "### 👀 Template Preview"
    )

    preview_rows = []

    for meal in preview_meals:

        preview_rows.append(
            [
                meal["meal_type"],
                meal["meal_time"],
                f"{meal['calories']} kcal",
                f"{meal['protein']} g",
                meal["food_items"]
            ]
        )


    preview_df = pd.DataFrame(
        preview_rows,
        columns=[
            "Meal",
            "Time",
            "Calories",
            "Protein",
            "Food Items"
        ]
    )

    st.dataframe(
        preview_df,
        use_container_width="stretch",
        hide_index=True
    )




    st.markdown(
        "#### 🌿 Ayurvedic Properties"
    )

    ayurvedic_preview = []

    for meal in preview_meals:

        ayurvedic_preview.append(
            [
                meal["meal_type"],
                meal["rasa"],
                meal["virya"],
                meal["digestion"]
            ]
        )

        ayurvedic_df = pd.DataFrame(
        ayurvedic_preview,
        columns=[
            "Meal",
            "Rasa",
            "Virya",
            "Digestion"
        ]
    )

    st.dataframe(
        ayurvedic_df,
        use_container_width="stretch",
        hide_index=True
    )


    # ======================================================
    # APPLY TEMPLATE TO PATIENT
    # ======================================================

    st.markdown("---")

    st.markdown(
        "### ➕ Apply Template to Patient"
    )

    if not patient_name:

        st.warning(
            "⚠️ Please select a patient first."
        )

    else:

        template_plan_name = st.text_input(
            "📄 New Diet Plan Name",
            value=f"{selected_template} Plan",
            placeholder="Enter diet plan name...",
            key="template_plan_name"
        )

        # ==========================================================
        # DIET PLAN SCHEDULE
        # ==========================================================

        st.markdown("### 📅 Diet Plan Schedule")

        schedule_col1, schedule_col2 = st.columns(2)

        with schedule_col1:

            start_date = st.date_input(
            "📅 Start Date",
            value=__import__("datetime").date.today(),
            key="diet_plan_start_date"
            )

        with schedule_col2:

            end_date = st.date_input(
            "📅 End Date",
            value=start_date,
            min_value=start_date,
            key="diet_plan_end_date"
            )

        duration_days = (
            end_date - start_date
        ).days + 1

        st.info(
           f"⏱️ Diet Plan Duration: **{duration_days} days**"
        )

        if st.button(
            "➕ Apply Template & Create Diet Plan",
            width="stretch",
            key="apply_template_to_current_plan"
        ):

            if not template_plan_name.strip():

                st.warning(
                "⚠️ Please enter a diet plan name."
            )

            elif end_date < start_date:

                st.warning(
                    "⚠️ End date cannot be before start date."
                )

            else:

                try:

                    # ==================================================
                    # STEP 1: CREATE NEW DIET PLAN
                    # ==================================================

                    diet_plan_id = create_new_diet_plan(
                        patient_name,
                        plan_name,
                        start_date.isoformat(),
                        end_date.isoformat(),
                        duration_days
                    )

                    # ==================================================
                    # STEP 2: APPLY TEMPLATE MEALS
                    # ==================================================

                    added_meals = apply_diet_plan_template(
                        diet_plan_id,
                        selected_template
                    )

                    # ==================================================
                    # STEP 3: SAVE CURRENT PLAN
                    # ==================================================

                    st.session_state.current_diet_plan_id = (
                        diet_plan_id
                    )

                    # ==================================================
                    # SUCCESS MESSAGE
                    # ==================================================

                    st.success(
                        f"✅ Diet plan '{template_plan_name}' "
                        f"created with {len(added_meals)} meals!"
                    )

                    st.info(
                        f"📅 Schedule: "
                        f"{start_date.strftime('%d/%m/%Y')} → "
                        f"{end_date.strftime('%d/%m/%Y')} "
                        f"({duration_days} days)"
                    )

                    st.rerun()

                except ValueError as error:

                    st.warning(
                        f"⚠️ {error}"
                    )

                except Exception as error:

                    st.error(
                        f"❌ Unable to create diet plan: {error}"
                    )


# ==========================================================
# MEAL INFORMATION
# ==========================================================

st.markdown("## 🍽️ Meal Information")

col1, col2, col3, col4 = st.columns(4)





# ==========================================================
# MEAL TYPE
# ==========================================================

with col1:

    meal_type = st.selectbox(
        "Meal",
        [
            "Breakfast",
            "Mid-Morning",
            "Lunch",
            "Evening Snack",
            "Dinner",
            "Bedtime"
        ]
    )


# ==========================================================
# MEAL TIME
# ==========================================================

with col2:

    meal_time = st.time_input(
        "Meal Time"
    )


# ==========================================================
# CALORIES
# ==========================================================

with col3:

    calories = st.number_input(
        "Calories",
        min_value=0,
        step=10
    )


# ==========================================================
# PROTEIN
# ==========================================================

with col4:

    protein = st.number_input(
        "Protein (g)",
        min_value=0.0,
        step=1.0
    )


# ==========================================================
# FOOD ITEMS
# ==========================================================

food_items = st.text_area(
    "🥗 Food Items",
    placeholder="Enter food items..."
)


# ==========================================================
# AYURVEDIC PROPERTIES
# ==========================================================

st.markdown("### 🌿 Ayurvedic Properties")

col1, col2, col3 = st.columns(3)


# ==========================================================
# RASA
# ==========================================================

with col1:

    rasa = st.selectbox(
        "Rasa (Taste)",
        [
            "Sweet",
            "Sour",
            "Salty",
            "Pungent",
            "Bitter",
            "Astringent"
        ]
    )


# ==========================================================
# VIRYA
# ==========================================================

with col2:

    virya = st.selectbox(
        "Virya",
        [
            "Hot",
            "Cold"
        ]
    )


# ==========================================================
# DIGESTION
# ==========================================================

with col3:

    digestion = st.selectbox(
        "Digestion",
        [
            "Easy",
            "Moderate",
            "Difficult"
        ]
    )


# ==========================================================
# MEAL NOTES
# ==========================================================

notes = st.text_area(
    "📝 Meal Notes",
    placeholder="Enter dietary notes..."
)


# ==========================================================
# ADD MEAL TO CURRENT PLAN
# ==========================================================

if st.session_state.current_diet_plan_id:

    st.markdown("---")

    st.markdown(
        "### 🍽️ Add Meal to Current Diet Plan"
    )

    if st.button(
        "➕ Add Meal",
        use_container_width="stretch"
    ):

        if not food_items.strip():

            st.warning(
                "⚠️ Please enter at least one food item."
            )

        else:

            try:

                add_meal_to_plan(
                    st.session_state.current_diet_plan_id,
                    meal_type,
                    meal_time.strftime("%H:%M"),
                    calories,
                    protein,
                    food_items,
                    rasa,
                    virya,
                    digestion,
                    notes
                )

                st.success(
                    f"✅ {meal_type} added to "
                    f"{plan_name}!"
                )

            except ValueError as error:

                st.warning(
                    f"⚠️ {error}"
                )

            except Exception as error:

                st.error(
                    f"❌ Something went wrong: {error}"
                )


# ==========================================================
# SHOW CURRENT DIET PLAN
# ==========================================================

if st.session_state.current_diet_plan_id:

    st.markdown("---")

    st.markdown(
        "## 📋 Current Diet Plan"
    )

    try:

        meals = fetch_diet_plan_meals(
            st.session_state.current_diet_plan_id
        )

        if meals:

            # ==================================================
            # DIET PLAN SUMMARY
            # ==================================================

            total_calories = sum(
                float(meal[3] or 0)
                for meal in meals
            )

            total_protein = sum(
                float(meal[4] or 0)
                for meal in meals
            )

            total_meals = len(meals)

            # ==================================================
            # NUTRITION SUMMARY
            # ==================================================

            st.markdown(
                "### 📊 Nutrition Summary"
            )

            summary_col1, summary_col2, summary_col3 = st.columns(3)

            with summary_col1:

                st.metric(
                    "🔥 Total Calories",
                    f"{total_calories:.0f} kcal"
                )

            with summary_col2:

                st.metric(
                    "💪 Total Protein",
                    f"{total_protein:.1f} g"
                )

            with summary_col3:

                st.metric(
                    "🍽️ Total Meals",
                    total_meals
                )

            st.markdown("---")

            # ==================================================
            # AYURVEDIC SUMMARY
            # ==================================================

            st.markdown(
                "### 🌿 Ayurvedic Overview"
            )

            rasa_values = [
                meal[6]
                for meal in meals
                if meal[6]
            ]

            virya_values = [
                meal[7]
                for meal in meals
                if meal[7]
            ]

            digestion_values = [
                meal[8]
                for meal in meals
                if meal[8]
            ]

            ayur_col1, ayur_col2, ayur_col3 = st.columns(3)

            with ayur_col1:

                st.write("**👅 Rasa**")

                if rasa_values:

                    st.write(
                        ", ".join(
                            dict.fromkeys(rasa_values)
                        )
                    )

                else:

                    st.write("Not specified")

            with ayur_col2:

                st.write("**🔥 Virya**")

                if virya_values:

                    st.write(
                        ", ".join(
                            dict.fromkeys(virya_values)
                        )
                    )

                else:

                    st.write("Not specified")

            with ayur_col3:

                st.write("**🍽️ Digestion**")

                if digestion_values:

                    st.write(
                        ", ".join(
                            dict.fromkeys(digestion_values)
                        )
                    )

                else:

                    st.write("Not specified")

            st.markdown("---")

            # ==================================================
            # MEAL LIST
            # ==================================================

            st.markdown(
                "### 🍽️ Meals"
            )

            for meal in meals:

                (
                    meal_id,
                    meal_type_saved,
                    meal_time_saved,
                    calories_saved,
                    protein_saved,
                    food_items_saved,
                    rasa_saved,
                    virya_saved,
                    digestion_saved,
                    notes_saved
                ) = meal

                # ==============================================
                # MEAL CARD
                # ==============================================

                st.markdown(
                    f"#### 🍽️ {meal_type_saved}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"⏰ **Time:** {meal_time_saved}"
                    )

                    st.write(
                        f"🔥 **Calories:** {calories_saved} kcal"
                    )

                with col2:

                    st.write(
                        f"💪 **Protein:** {protein_saved} g"
                    )

                    st.write(
                        f"🥗 **Food:** {food_items_saved}"
                    )

                with col3:

                    st.write(
                        f"🌿 **Rasa:** {rasa_saved}"
                    )

                    st.write(
                        f"🔥 **Virya:** {virya_saved}"
                    )

                    st.write(
                        f"🍽️ **Digestion:** {digestion_saved}"
                    )

                if notes_saved:

                    st.write(
                        f"📝 **Notes:** {notes_saved}"
                    )

                # ==============================================
                # EDIT / DELETE BUTTONS
                # ==============================================

                edit_col, delete_col = st.columns(2)

                with edit_col:

                    edit_clicked = st.button(
                        "✏️ Edit",
                        key=f"edit_meal_{meal_id}",
                        use_container_width="stretch"
                    )

                with delete_col:

                    delete_clicked = st.button(
                        "🗑️ Delete",
                        key=f"delete_meal_{meal_id}",
                        use_container_width="stretch"
                    )

                # ==============================================
                # DELETE MEAL
                # ==============================================

                if delete_clicked:

                    try:

                        delete_meal(
                            meal_id
                        )

                        st.success(
                            "✅ Meal deleted successfully."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"❌ Unable to delete meal: {error}"
                        )

                # ==============================================
                # OPEN EDIT MODE
                # ==============================================

                if edit_clicked:

                    st.session_state[
                        f"editing_meal_{meal_id}"
                    ] = True

                # ==============================================
                # EDIT FORM
                # ==============================================

                if st.session_state.get(
                    f"editing_meal_{meal_id}",
                    False
                ):

                    st.markdown(
                        "#### ✏️ Edit Meal"
                    )

                    edit_col1, edit_col2 = st.columns(2)

                    # ==========================================
                    # EDIT LEFT
                    # ==========================================

                    with edit_col1:

                        meal_options = [
                            "Breakfast",
                            "Mid-Morning",
                            "Lunch",
                            "Evening Snack",
                            "Dinner",
                            "Bedtime"
                        ]

                        current_meal_index = (
                            meal_options.index(
                                meal_type_saved
                            )
                            if meal_type_saved in meal_options
                            else 0
                        )

                        edited_meal_type = st.selectbox(
                            "Meal Type",
                            meal_options,
                            index=current_meal_index,
                            key=f"edit_type_{meal_id}"
                        )

                        edited_calories = st.number_input(
                            "Calories",
                            min_value=0,
                            value=int(
                                calories_saved or 0
                            ),
                            step=10,
                            key=f"edit_calories_{meal_id}"
                        )

                        edited_protein = st.number_input(
                            "Protein (g)",
                            min_value=0.0,
                            value=float(
                                protein_saved or 0
                            ),
                            step=1.0,
                            key=f"edit_protein_{meal_id}"
                        )

                    # ==========================================
                    # EDIT RIGHT
                    # ==========================================

                    with edit_col2:

                        edited_meal_time = st.text_input(
                            "Meal Time",
                            value=str(
                                meal_time_saved
                            ),
                            key=f"edit_time_{meal_id}"
                        )

                        edited_food_items = st.text_area(
                            "Food Items",
                            value=str(
                                food_items_saved or ""
                            ),
                            key=f"edit_food_{meal_id}"
                        )

                        edited_notes = st.text_area(
                            "Notes",
                            value=str(
                                notes_saved or ""
                            ),
                            key=f"edit_notes_{meal_id}"
                        )

                    # ==========================================
                    # EDIT AYURVEDIC PROPERTIES
                    # ==========================================

                    edit_col3, edit_col4, edit_col5 = st.columns(3)

                    rasa_options = [
                        "Sweet",
                        "Sour",
                        "Salty",
                        "Pungent",
                        "Bitter",
                        "Astringent"
                    ]

                    digestion_options = [
                        "Easy",
                        "Moderate",
                        "Difficult"
                    ]

                    with edit_col3:

                        current_rasa_index = (
                            rasa_options.index(
                                rasa_saved
                            )
                            if rasa_saved in rasa_options
                            else 0
                        )

                        edited_rasa = st.selectbox(
                            "Rasa",
                            rasa_options,
                            index=current_rasa_index,
                            key=f"edit_rasa_{meal_id}"
                        )

                    with edit_col4:

                        edited_virya = st.selectbox(
                            "Virya",
                            [
                                "Hot",
                                "Cold"
                            ],
                            index=(
                                1
                                if virya_saved == "Cold"
                                else 0
                            ),
                            key=f"edit_virya_{meal_id}"
                        )

                    with edit_col5:

                        current_digestion_index = (
                            digestion_options.index(
                                digestion_saved
                            )
                            if digestion_saved in digestion_options
                            else 0
                        )

                        edited_digestion = st.selectbox(
                            "Digestion",
                            digestion_options,
                            index=current_digestion_index,
                            key=f"edit_digestion_{meal_id}"
                        )

                    # ==========================================
                    # SAVE / CANCEL
                    # ==========================================

                    save_col, cancel_col = st.columns(2)

                    with save_col:

                        save_edit = st.button(
                            "💾 Save Changes",
                            key=f"save_edit_{meal_id}",
                            use_container_width="stretch"
                        )

                    with cancel_col:

                        cancel_edit = st.button(
                            "❌ Cancel",
                            key=f"cancel_edit_{meal_id}",
                            use_container_width="stretch"
                        )

                    # ==========================================
                    # SAVE EDIT
                    # ==========================================

                    if save_edit:

                        try:

                            update_meal(
                                meal_id,
                                edited_meal_type,
                                edited_meal_time,
                                edited_calories,
                                edited_protein,
                                edited_food_items,
                                edited_rasa,
                                edited_virya,
                                edited_digestion,
                                edited_notes
                            )

                            st.success(
                                "✅ Meal updated successfully."
                            )

                            st.session_state[
                                f"editing_meal_{meal_id}"
                            ] = False

                            st.rerun()

                        except ValueError as error:

                            st.warning(
                                f"⚠️ {error}"
                            )

                        except Exception as error:

                            st.error(
                                f"❌ Unable to update meal: {error}"
                            )

                    # ==========================================
                    # CANCEL EDIT
                    # ==========================================

                    if cancel_edit:

                        st.session_state[
                            f"editing_meal_{meal_id}"
                        ] = False

                        st.rerun()

                st.markdown("---")

        else:

            st.info(
                "ℹ️ No meals added to this diet plan yet."
            )

    except Exception as error:

        st.error(
            f"❌ Unable to load meals: {error}"
        )
# ==========================================================
# PATIENT DIET HISTORY
# ==========================================================

st.markdown("---")

st.markdown(
    "## 📜 Patient Diet History"
)

if patient_name:

    try:

        # ==================================================
        # FETCH PATIENT HISTORY
        # ==================================================

        diet_history = fetch_patient_diet_history(
            patient_name
        )

        # ==================================================
        # HISTORY SUMMARY
        # ==================================================

        history_summary = get_patient_history_summary(
            patient_name
        )

        history_col1, history_col2, history_col3, history_col4 = (
            st.columns(4)
        )

        with history_col1:

            st.metric(
                "📋 Total Plans",
                history_summary["total_plans"]
            )

        with history_col2:

            st.metric(
                "🟢 Active",
                history_summary["active_plans"]
            )

        with history_col3:

            st.metric(
                "⏸️ Paused",
                history_summary["paused_plans"]
            )

        with history_col4:

            st.metric(
                "✅ Completed",
                history_summary["completed_plans"]
            )

        # ==================================================
        # HISTORY TABLE
        # ==================================================

        if diet_history:

            history_rows = []

            for history in diet_history:

                history_rows.append(
                    [
                        history["plan_name"],
                        history["status"],
                        history["created_at"],
                        history["updated_at"],
                        history["meal_count"],
                        f"{history['total_calories']:.0f} kcal",
                        f"{history['total_protein']:.1f} g"
                    ]
                )

            history_df = pd.DataFrame(
                history_rows,
                columns=[
                    "Plan Name",
                    "Status",
                    "Created",
                    "Updated",
                    "Meals",
                    "Calories",
                    "Protein"
                ]
            )

            st.dataframe(
                history_df,
                width="stretch",
                hide_index=True
            )

            # ==============================================
            # OPEN PREVIOUS PLAN
            # ==============================================

            st.markdown(
                "### 📂 Open Previous Diet Plan"
            )

            history_options = {}

            for history in diet_history:

                label = (
                    f"{history['plan_name']} | "
                    f"{history['status']} | "
                    f"{history['created_at']}"
                )

                history_options[label] = (
                    history["plan_id"]
                )

            selected_history_label = st.selectbox(
                "Select a previous diet plan",
                list(history_options.keys()),
                index=None,
                placeholder="Choose a diet plan...",
                key="history_plan_selector"
            )

            if selected_history_label:

                selected_history_plan_id = (
                    history_options[
                        selected_history_label
                    ]
                )

                if st.button(
                    "📂 Open Previous Plan",
                    width="stretch",
                    key="open_history_plan"
                ):

                    st.session_state.current_diet_plan_id = (
                        selected_history_plan_id
                    )

                    st.success(
                        "✅ Previous diet plan opened successfully!"
                    )

                    st.rerun()

        else:

            st.info(
                "ℹ️ This patient has no diet plan history yet."
            )

    except Exception as error:

        st.error(
            f"❌ Unable to load diet history: {error}"
        )

else:

    st.info(
        "👤 Select a patient to view diet history."
    )


# ==========================================================
# FOOTER
# ==========================================================

footer()
