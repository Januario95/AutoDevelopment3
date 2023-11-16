from access_page import main

main()


from verify_remaining import fetch_remaining_rows, save_df_and_merge

print('STARTING TO FETCH REMAINING ROWS========================')
for i in range(4):
    fetch_remaining_rows(driver)
    time.sleep(2)

    print('MERGING AND SAVING FILES================================')
    save_df_and_merge()
    time.sleep(3)

from search_process import search_client_process 
print('SWITCHING TO PARENT NODE================================')
driver.switch_to.parent_frame()
print('STARGING TO SEARCH PROPOSALS============================')
for i in range(4):
    search_client_process(driver)
    time.sleep(2)
