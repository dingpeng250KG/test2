drop database if exists fangtx;

create database fangtx default charset utf8 collate utf8_bin;
	
use fangtx;

/* 创建经理人表 */
create table tb_agent
(
   agentid              int not null auto_increment,
   name                 varchar(255) not null,
   tel                  varchar(20) not null,
   servstar             int not null default 0,
   realstar             int not null default 0,
   profstar             int not null default 0,
   certificated         bool not null default 0,
   primary key (agentid)
);

/* 创建经理人楼盘中间表 */
create table tb_agent_estate
(
   agent_estate_id      int not null auto_increment,
   agentid              int not null,
   estateid             int not null,
   primary key (agent_estate_id)
);

/* 创建地区表 */
create table tb_district
(
   distid               int not null,
   pid                  int,
   name                 varchar(255) not null,
   intro                varchar(255) default '',
   primary key (distid)
);

/* 创建楼盘表 */
create table tb_estate
(
   estateid             int not null auto_increment,
   distid               int not null,
   name                 varchar(255) not null,
   hot                  int default 0,
   intro                varchar(511) default '',
   primary key (estateid)
);

/* 创建房源信息表 */
create table tb_house_info
(
   houseid              int not null auto_increment,
   title                varchar(50) not null,
   area                 int not null,
   floor                int not null,
   totalfloor           int not null,
   direction            varchar(10) not null,
   price                int not null,
   priceunit            varchar(10) not null,
   detail               varchar(511) default '',
   mainphoto            varchar(255) not null,
   pubdate              timestamp not null default now(),
   street               varchar(255) not null,
   hassubway            bool not null default 0,
   isshared             bool not null default 0,
   hasagentfees         bool not null default 0,
   typeid               int not null,
   userid               int not null,
   distid               int not null,
   estateid             int,
   agentid              int,
   primary key (houseid)
);

/* 创建房源照片表 */
create table tb_house_photo
(
   photoid              int not null auto_increment,
   houseid              int not null,
   path                 varchar(255) not null,
   primary key (photoid)
);

/* 创建房源标签中间表 */
create table tb_house_tag
(
   house_tag_id         int not null auto_increment,
   houseid              int not null,
   tagid                int not null,
   primary key (house_tag_id)
);

/* 创建户型表 */
create table tb_house_type
(
   typeid               int not null,
   name                 varchar(255) not null,
   primary key (typeid)
);

/* 创建登录日志表 */
create table tb_login_log
(
   logid                bigint not null auto_increment,
   userid               int not null,
   ipaddr               varchar(255) not null,
   logdate              timestamp not null default now(),
   devcode              varchar(255) not null default '',
   primary key (logid)
);

/* 创建用户浏览历史记录表 */
create table tb_record
(
   recordid             bigint not null auto_increment,
   userid               int not null,
   houseid              int not null,
   recorddate           timestamp not null default now(),
   primary key (recordid)
);

/* 创建标签表 */
create table tb_tag
(
   tagid                int not null auto_increment,
   name                 varchar(20) not null,
   primary key (tagid)
);

/* 创建用户表 */
create table tb_user
(
   userid               int not null auto_increment,
   username             varchar(20) not null,
   password             char(32) not null,
   realname             varchar(20) not null,
   tel                  varchar(20) not null,
   email                varchar(255) not null,
   createdate           timestamp not null default now(),
   point                int not null default 0,
   lastvisit            timestamp not null default now(),
   is_authenticated     bit not null default 0,
   primary key (userid)
);

/* 创建用户令牌表 */
create table tb_user_token
(
   tokenid              int not null auto_increment,
   token                char(32) not null,
   userid               int not null,
   primary key (tokenid)
);

/* 创建权限表 */
create table tb_privilege
(
   privid               integer auto_increment not null,
   url                  varchar(1024) not null,
   method               varchar(15) not null,
   PRIMARY KEY (privid)
);

/* 创建角色表 */
create table tb_role
(
   roleid               integer auto_increment not null,
   rolename             varchar(255) not null,
   primary key (roleid)
);

/* 创建角色权限中间表 */
create table tb_role_privilege
(
   rpid                 integer auto_increment not null,
   privid               integer not null,
   roleid               integer not null,
   primary key (rpid)
);

/* 创建用户角色中间表 */
create table tb_user_role
(
   urid                 integer auto_increment not null,
   roleid               integer not null,
   userid               integer not null,
   primary key (urid)
);

create unique index uni_idx_agent_estate on tb_agent_estate (agentid, estateid);

create unique index uni_idx_record on tb_record (userid, houseid);

create unique index uni_idx_userid on tb_user_token (userid);

create unique index uni_idx_username on tb_user (username);

create unique index uni_idx_tel on tb_user (tel);

create unique index uni_idx_email on tb_user (email);

create unique index uni_idx_house_tag on tb_house_tag (houseid, tagid);

alter table tb_agent_estate add constraint fk_agent_estate_agentid foreign key (agentid) references tb_agent (agentid) on delete restrict on update restrict;

alter table tb_agent_estate add constraint fk_agent_estate_estateid foreign key (estateid) references tb_estate (estateid) on delete restrict on update restrict;

alter table tb_district add constraint fk_district_pid foreign key (pid) references tb_district (distid) on delete restrict on update restrict;

alter table tb_estate add constraint fk_estate_distid foreign key (distid) references tb_district (distid) on delete restrict on update restrict;

alter table tb_house_info add constraint fk_house_info_agentid foreign key (agentid) references tb_agent (agentid) on delete restrict on update restrict;

alter table tb_house_info add constraint fk_house_info_distid foreign key (distid) references tb_district (distid) on delete restrict on update restrict;

alter table tb_house_info add constraint fk_house_info_estateid foreign key (estateid) references tb_estate (estateid) on delete restrict on update restrict;

alter table tb_house_info add constraint fk_house_info_typeid foreign key (typeid) references tb_house_type (typeid) on delete restrict on update restrict;

alter table tb_house_info add constraint fk_house_info_userid foreign key (userid) references tb_user (userid) on delete restrict on update restrict;

alter table tb_house_photo add constraint fk_house_photo_houseid foreign key (houseid) references tb_house_info (houseid) on delete restrict on update restrict;

alter table tb_house_tag add constraint fk_house_tag_houseid foreign key (houseid) references tb_house_info (houseid) on delete restrict on update restrict;

alter table tb_house_tag add constraint fk_house_tag_tagid foreign key (tagid) references tb_tag (tagid) on delete restrict on update restrict;

alter table tb_login_log add constraint fk_login_log_userid foreign key (userid) references tb_user (userid) on delete restrict on update restrict;

alter table tb_record add constraint fk_record_houseid foreign key (houseid) references tb_house_info (houseid) on delete restrict on update restrict;

alter table tb_record add constraint fk_record_userid foreign key (userid) references tb_user (userid) on delete restrict on update restrict;
			
alter table tb_user_token add constraint fk_token_userid foreign key (userid) references tb_user (userid) on delete restrict on update restrict;

alter table tb_user_role add constraint uni_user_role unique (userid, roleid);

alter table tb_role_privilege add constraint uni_role_priv unique (roleid, privid);

alter table tb_role_privilege add constraint fk_role_privilege_privid foreign key (privid) references tb_privilege (privid);

alter table tb_role_privilege add constraint fk_role_privilege_roleid foreign key (roleid) references tb_role (roleid);

alter table tb_user_role add constraint fk_user_role_roleid foreign key (roleid) references tb_role (roleid);

alter table tb_user_role add constraint fk_user_role_userid foreign key (userid) references tb_user (userid);
