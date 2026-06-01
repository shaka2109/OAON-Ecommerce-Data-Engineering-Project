# Databricks notebook source
resources:
  jobs:
    oaon_bronze_load:

      name: OAON Bronze Load

      tasks:

        - task_key: CostCenter_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/CostCenter_Bronze

        - task_key: Currency_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/Currency_Bronze

        - task_key: CustTable_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/CustTable_Bronze

        - task_key: FiscalPeriod_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/FiscalPeriod_Bronze

        - task_key: Parties_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/Parties_Bronze

        - task_key: PartyAddress_bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/PartyAddress_bronze

        - task_key: PromoTable_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/PromoTable_Bronze

        - task_key: PurchaseOrder_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/PurchaseOrder_Bronze

        - task_key: PurchCategory_bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/PurchCategory_bronze

        - task_key: PurchContracts_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/PurchContracts_Bronze

        - task_key: PurchItem_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/PurchItem_Bronze

        - task_key: SalesOrderLine_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/SalesOrderLine_Bronze

        - task_key: VendTable_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/VendTable_Bronze

        - task_key: WorkerTable_Bronze
          notebook_task:
            notebook_path: ../notebooks/Bronze/WorkerTable_Bronze
