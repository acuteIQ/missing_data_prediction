function [ output ] = get_single_sql_result( conn, sql_cmd )
    data = select(conn, sql_cmd);
    output = data{1,1};
end

