# Databricks notebook source
resources:
  jobs:
    oaon_raw_load:

      name: OAON Raw Load

      tasks:

        - task_key: CostCenter
          notebook_task:
            notebook_path: ../notebooks/Raw/CostCenter

        - task_key: Currency
          notebook_task:
            notebook_path: ../notebooks/Raw/Currency

        - task_key: CustTable
          notebook_task:
            notebook_path: ../notebooks/Raw/CustTable

        - task_key: Fiscalperiod
          notebook_task:
            notebook_path: ../notebooks/Raw/Fiscalperiod

        - task_key: Parties
          notebook_task:
            notebook_path: ../notebooks/Raw/Parties

        - task_key: PartyAddress
          notebook_task:
            notebook_path: ../notebooks/Raw/PartyAddress

        - task_key: PromoTable
          notebook_task:
            notebook_path: ../notebooks/Raw/PromoTable

        - task_key: PurchaseOrder
          notebook_task:
            notebook_path: ../notebooks/Raw/PurchaseOrder

        - task_key: PurchCategory
          notebook_task:
            notebook_path: ../notebooks/Raw/PurchCategory

        - task_key: PurchContracts
          notebook_task:
            notebook_path: ../notebooks/Raw/PurchContracts

        - task_key: PurchItem
          notebook_task:
            notebook_path: ../notebooks/Raw/CustTable

        - task_key: SalesOrderLine
          notebook_task:
            notebook_path: ../notebooks/Raw/SalesOrderLine

        - task_key: VendTable
          notebook_task:
            notebook_path: ../notebooks/Raw/VendTable

        - task_key: WorkerTable
          notebook_task:
            notebook_path: ../notebooks/Raw/WorkerTable
        
