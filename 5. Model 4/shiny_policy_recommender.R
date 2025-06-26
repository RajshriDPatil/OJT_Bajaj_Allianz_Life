# app.R (fixed version)

options(shiny.maxRequestSize = 300*1024^2)  # 300 MB file upload

library(shiny)
library(dplyr)
library(arules)

ui <- fluidPage(
  titlePanel("\U0001F50D Insurance Policy Recommendation System"),
  
  sidebarLayout(
    sidebarPanel(
      fileInput("file", "Upload Insurance CSV", accept = ".csv"),
      tags$hr(),
      
      selectInput("Premium_term", "Select Premium Term (in years):", choices = seq(5, 60, 5)),
      selectInput("Age_group", "Select Age Group:", choices = c("18-30", "31-40", "41-50", "51-60")),
      selectInput("Income_group", "Select Income Group:", choices = c("0-3L", "3-6L", "6-10L", "10L+")),
      selectInput("Gender", "Gender:", choices = c("male", "female")),
      selectInput("Location", "Location:", choices = c("rural", "semi-urban", "urban")),
      selectInput("Current_status", "Current Marital Status:", choices = c("married", "unmarried", "widow")),
      selectInput("booking", "Booking Frequency:", choices = c("Monthly", "Quarterly", "Half_yearly", "Yearly")),
      
      actionButton("recommend", "Get Recommendation")
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel("\U0001F4CA Data Summary",
                 tags$div(style = "background-color: #fdfdfd; padding: 20px; border-radius: 12px; box-shadow: 0 0 8px rgba(0,0,0,0.1);",
                          h4("\U0001F4CC Summary Statistics", style = "font-weight: bold;"),
                          verbatimTextOutput("summary_output"),
                          plotOutput("hist_age"), textOutput("conclusion_age"),
                          plotOutput("hist_income"), textOutput("conclusion_income"),
                          plotOutput("hist_premium_term"), textOutput("conclusion_premium_term"),
                          h4("Gender"), plotOutput("hist_gender"), textOutput("conclusion_gender"),
                          h4("Booking Frequency"), plotOutput("hist_booking"), textOutput("conclusion_booking"),
                          h4("Location"), plotOutput("hist_location"), textOutput("conclusion_location"),
                          h4("Current Status"), plotOutput("hist_status"), textOutput("conclusion_status")
                 )
        ),
        tabPanel("\U0001F4C8 Recommendations",
                 tags$div(
                   style = "background-color: #f9f9f9; padding: 20px; border-radius: 12px; box-shadow: 0 0 10px rgba(0,0,0,0.1);",
                   h4("\U0001F3AF Recommended Policies", style = "color: #333; font-weight: bold;"),
                   tags$div(
                     style = "background-color: #fff; padding: 10px; border-left: 4px solid #007bff; margin-bottom: 10px;",
                     verbatimTextOutput("recommendation_output")
                   ),
                   tags$div(
                     style = "background-color: #ffffff; padding: 10px; border-radius: 8px;",
                     tableOutput("rule_table")
                   )
                 )
        )
      )
    )
  )
)

server <- function(input, output, session) {
  
  insurance_data <- reactive({
    req(input$file)
    df <- read.csv(input$file$datapath, stringsAsFactors = FALSE)
    
    required_cols <- c("age", "gender", "declared_income", "premium_term", "policy_term",
                       "premium_amount", "booking_frequency", "location",
                       "policy_type", "current_status")
    
    missing_cols <- setdiff(required_cols, names(df))
    if (length(missing_cols) > 0) {
      showModal(modalDialog(
        title = "Missing Columns",
        paste("The following required columns are missing:", paste(missing_cols, collapse = ", ")),
        easyClose = TRUE
      ))
      return(NULL)
    }
    
    df <- df %>%
      mutate(
        age = as.numeric(age),
        declared_income = as.numeric(declared_income),
        age_group = cut(age, breaks = c(17, 30, 40, 50, 60), labels = c("18-30", "31-40", "41-50", "51-60")),
        income_group = case_when(
          declared_income <= 300000 ~ "0-3L",
          declared_income <= 600000 ~ "3-6L",
          declared_income <= 1000000 ~ "6-10L",
          TRUE ~ "10L+"
        ),
        premium_term = paste0("premium_term=", premium_term),
        policy_term = paste0("policy_term=", policy_term),
        booking_frequency = paste0("booking=", booking_frequency),
        gender = paste0("gender=", gender),
        location = paste0("location=", location),
        age_group = paste0("age_group=", age_group),
        income_group = paste0("income=", income_group),
        policy_type = paste0("policy_type=", policy_type),
        current_status = paste0("current_status=", current_status)
      )
    
    return(df)
  })
  
  output$summary_output <- renderPrint({
    req(insurance_data())
    summary(insurance_data())
  })
  
  output$hist_age <- renderPlot({
    req(insurance_data())
    hist(insurance_data()$age, col = "skyblue", main = "Age Distribution", xlab = "Age")
  })
  output$conclusion_age <- renderText({
    req(insurance_data())
    paste("Most users are in age group:",
          names(which.max(table(cut(insurance_data()$age, breaks = c(17, 30, 40, 50, 60)))))
    )
  })
  
  output$hist_income <- renderPlot({
    req(insurance_data())
    hist(insurance_data()$declared_income, col = "lightgreen", main = "Declared Income", xlab = "INR")
  })
  output$conclusion_income <- renderText({
    req(insurance_data())
    paste("Most users fall in income group:", names(which.max(table(insurance_data()$income_group))))
  })
  
  output$hist_premium_term <- renderPlot({
    req(insurance_data())
    terms <- as.numeric(gsub("premium_term=", "", insurance_data()$premium_term))
    hist(terms, col = "tomato", main = "Premium Term Distribution", xlab = "Years")
  })
  output$conclusion_premium_term <- renderText({
    req(insurance_data())
    terms <- gsub("premium_term=", "", insurance_data()$premium_term)
    paste("Most users selected premium term:", names(which.max(table(terms))), "years.")
  })
  
  output$hist_gender <- renderPlot({
    req(insurance_data())
    barplot(table(insurance_data()$gender), col = "lightblue", main = "Gender Distribution")
  })
  output$conclusion_gender <- renderText({
    req(insurance_data())
    most <- names(which.max(table(insurance_data()$gender)))
    paste("Most users are", gsub("gender=", "", most))
  })
  
  output$hist_booking <- renderPlot({
    req(insurance_data())
    barplot(table(insurance_data()$booking_frequency), col = "plum", main = "Booking Frequency")
  })
  output$conclusion_booking <- renderText({
    req(insurance_data())
    most <- names(which.max(table(insurance_data()$booking_frequency)))
    paste("Most users prefer", gsub("booking=", "", most), "booking")
  })
  
  output$hist_location <- renderPlot({
    req(insurance_data())
    barplot(table(insurance_data()$location), col = "orange", main = "Location Distribution")
  })
  output$conclusion_location <- renderText({
    req(insurance_data())
    most <- names(which.max(table(insurance_data()$location)))
    paste("Most users are from", gsub("location=", "", most), "areas")
  })
  
  output$hist_status <- renderPlot({
    req(insurance_data())
    barplot(table(insurance_data()$current_status), col = "salmon", main = "Marital Status")
  })
  output$conclusion_status <- renderText({
    req(insurance_data())
    most <- names(which.max(table(insurance_data()$current_status)))
    paste("Most users are", gsub("current_status=", "", most))
  })
  
  observeEvent(input$recommend, {
    req(insurance_data())
    
    filtered_data <- insurance_data() %>%
      filter(
        age_group == paste0("age_group=", input$Age_group),
        income_group == paste0("income=", input$Income_group),
        gender == paste0("gender=", input$Gender),
        location == paste0("location=", input$Location),
        current_status == paste0("current_status=", input$Current_status),
        booking_frequency == paste0("booking=", input$booking)
      )
    
    if (nrow(filtered_data) == 0) {
      output$recommendation_output <- renderText("No matching records found for the selected filters.")
      output$rule_table <- renderTable(NULL)
      return()
    }
    
    trans_data <- filtered_data %>%
      select(premium_term, policy_term, booking_frequency, gender, location,
             age_group, income_group, policy_type, current_status)
    item_list <- apply(trans_data, 1, as.character)
    transactions <- as(split(item_list, seq(nrow(trans_data))), "transactions")
    
    rules <- apriori(transactions, parameter = list(supp = 0.05, conf = 0.6))
    
    selected_term <- paste0("premium_term=", input$Premium_term)
    filtered_rules <- subset(rules, lhs %pin% selected_term & rhs %pin% "policy_term=")
    
    if (length(filtered_rules) == 0) {
      output$recommendation_output <- renderText({
        paste("\u26A0\uFE0F No rules found. Showing fallback for Premium Term", input$Premium_term)
      })
      fallback <- filtered_data %>%
        filter(premium_term == selected_term) %>%
        count(policy_term) %>%
        arrange(desc(n)) %>%
        slice(1)
      output$rule_table <- renderTable({
        if (nrow(fallback) == 0) {
          data.frame(Rule = "No fallback available.", Confidence = NA, Lift = NA)
        } else {
          data.frame(
            Rule = paste0("premium_term=", input$Premium_term, " => ", fallback$policy_term),
            Confidence = "Fallback",
            Lift = "-"
          )
        }
      })
    } else {
      rule_df <- as(filtered_rules, "data.frame")
      rule_df$Rule <- sapply(seq_along(filtered_rules), function(i) {
        lhs <- labels(lhs(filtered_rules[i]))[[1]]
        rhs_items <- unlist(LIST(rhs(filtered_rules[i])))
        rhs_selected <- rhs_items[grepl("policy_term=|policy_type=|booking=|age_group=", rhs_items)]
        paste(lhs, "=>", paste(rhs_selected, collapse = ", "))
      })
      
      rule_df <- rule_df %>%
        arrange(desc(confidence * lift)) %>%
        mutate(
          Confidence = round(confidence, 2),
          Lift = round(lift, 2)
        )
      
      output$recommendation_output <- renderText({
        paste("\u2705 Recommendations for Premium Term", input$Premium_term)
      })
      output$rule_table <- renderTable({
        rule_df[, c("Rule", "Confidence", "Lift")]
      }, striped = TRUE, hover = TRUE, bordered = TRUE)
    }
  })
}

shinyApp(ui, server)
