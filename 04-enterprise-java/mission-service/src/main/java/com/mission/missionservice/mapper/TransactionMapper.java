package com.mission.missionservice.mapper;

import com.mission.missionservice.entity.Transaction;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

// Given - the interface for Kata B (XML-based). You'll write the SQL in
// TransactionMapper.xml, not here.
@Mapper
public interface TransactionMapper {

    List<Transaction> findByAccountId(int accountId);
}
