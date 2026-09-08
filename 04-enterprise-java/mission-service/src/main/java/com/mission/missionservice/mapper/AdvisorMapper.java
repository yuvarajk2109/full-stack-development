package com.mission.missionservice.mapper;

import com.mission.missionservice.entity.Advisor;
import org.apache.ibatis.annotations.Select;

public interface AdvisorMapper {

    @Select("SELECT advisor_id, name, region FROM advisors WHERE advisor_id = #{advisorId}")
    Advisor findById(int advisorId);
}
