$(function () {
    dtable = new webix.ui({
        container: "browsetable",
        id: "dtable",
        view: "datatable",
        css:"dormancybase_table protein_link",
        columns: [
            {id: "species", map: "#data1#", header: ["Species", {content: "selectFilter"}], width: 300},
            {id: "seqname", map: "#data2#", header: ["Sequence name", {content: "textFilter"}], width: 350},
            {id: "dormancytype", map: "#data3#", header: ["Dormancy type", {content: "selectFilter"}], width: 150},
            {id: "lifestage", map: "#data4#", header: ["Life stage", {content: "selectFilter"}], width: 150},
            {id: "numexp", map: "#data5#", header: ["Number of","Samples"], width: 150},
            {id: "dbid", map: "#data6#", header: ["ID"], width: 150, hidden:true}
        ],
        resizeColumn: true,
        datatype: "csv",
        url: data_url_prefix+'data/brows.csv',
        autoheight: true,
        autowidth: true,
        pager: {
            css:"dormancybase_table",
            template: "{common.prev()}{common.next()}Page {common.page()} from #limit#",
            container: "paging_here",
            size: 25,
            group: 5
        },
        hover: "browse_row_hover",
        on: {
            "onItemClick": function (id, e, trg) {
                window.location.href = data_url_prefix+"sequence/"+dtable.getItem(id.row).dbid+".html";
            }
        }
    });
    $(window).resize(function() {
        if ($(window).width() < 1200){
            dtable.hideColumn("numexp");
            dtable.setColumnWidth("species", 200);
            dtable.setColumnWidth("seqname", 200);
        }
        if ($(window).width() < 800){
            dtable.setColumnWidth("species", 150);
            dtable.setColumnWidth("seqname", 150);
            dtable.setColumnWidth("dormancytype", 80);
            dtable.setColumnWidth("lifestage", 80);
        }
        if ($(window).width() >= 800){
            dtable.setColumnWidth("species", 200);
            dtable.setColumnWidth("seqname", 200);
            dtable.setColumnWidth("dormancytype", 150);
            dtable.setColumnWidth("lifestage", 150);
        }
        if ($(window).width() >= 1200){
            dtable.showColumn("numexp");
            dtable.setColumnWidth("species", 300);
            dtable.setColumnWidth("seqname", 350);
        }
    });
    if ($(window).width() < 1200){
        dtable.hideColumn("numexp");
        dtable.setColumnWidth("species", 200);
        dtable.setColumnWidth("seqname", 200);
    }
    if ($(window).width() < 800){
        dtable.setColumnWidth("species", 150);
        dtable.setColumnWidth("seqname", 150);
        dtable.setColumnWidth("dormancytype", 80);
        dtable.setColumnWidth("lifestage", 80);
    }
});
