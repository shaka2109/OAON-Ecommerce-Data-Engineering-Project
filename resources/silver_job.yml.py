# Databricks notebook source
resources:
  jobs:
    oaon_silver_load:

      name: OAON Silver Load

      tasks:

        - task_key: DimCostCenter_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimCostCenter_Silver

        - task_key: DimCurrency_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimCurrency_Silver

        - task_key: DimCustTable_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimCustTable_Silver

        - task_key: DimDate_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimDate_Silver

        - task_key: DimParty_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimParty_Silver

        - task_key: DimPaymentTypes_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimPaymentTypes_Silver

        - task_key: DimPromoTable_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimPromoTable_Silver

        - task_key: DimPurchCategory_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimPurchCategory_Silver

        - task_key: DimPurchItem_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimPurchItem_Silver

        - task_key: DimVendor_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimVendor_Silver

        - task_key: DimVertical_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimVertical_Silver

        - task_key: DimWorkerTable_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/DimWorkerTable_Silver

        - task_key: FactPurchaseOrder_Silver

          depends_on:
            - task_key: DimCostCenter_Silver
            - task_key: DimCurrency_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/FactPurchaseOrder_Silver

        - task_key: FactSalesOrderLine_Silver

          notebook_task:
            notebook_path: ../notebooks/Silver/FactSalesOrderLine_Silver
